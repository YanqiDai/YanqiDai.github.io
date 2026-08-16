#!/usr/bin/env ruby

require "yaml"
require "cgi"
require "fileutils"

Token = Struct.new(:type, :value)

def tokenize(source)
  source.split(/(\{\{.*?\}\}|\{%.*?%\})/m).reject(&:empty?).map do |part|
    if part.start_with?("{{")
      Token.new(:output, part[2...-2].strip)
    elsif part.start_with?("{%"); Token.new(:tag, part[2...-2].strip)
    else Token.new(:text, part)
    end
  end
end

def parse_nodes(tokens, index = 0, stops = [])
  nodes = []
  while index < tokens.length
    token = tokens[index]
    if token.type == :tag
      name = token.value.split.first
      return [nodes, index, token.value] if stops.include?(name)

      case name
      when "for"
        match = token.value.match(/\Afor\s+(\w+)\s+in\s+(.+)\z/)
        raise "Unsupported for tag: #{token.value}" unless match
        body, end_index, end_tag = parse_nodes(tokens, index + 1, ["endfor"])
        raise "Missing endfor for: #{token.value}" unless end_tag.start_with?("endfor")
        nodes << [:for, match[1], match[2].strip, body]
        index = end_index
      when "if", "unless"
        condition = token.value.sub(/\A(?:if|unless)\s+/, "")
        truthy, branch_index, branch_stop = parse_nodes(tokens, index + 1, ["else", "endif", "endunless"])
        falsy = []
        if branch_stop.start_with?("else")
          falsy, branch_index, branch_stop = parse_nodes(tokens, branch_index + 1, ["endif", "endunless"])
        end
        expected_end = name == "if" ? "endif" : "endunless"
        raise "Missing #{expected_end} for: #{token.value}" unless branch_stop.start_with?(expected_end)
        nodes << [name.to_sym, condition, truthy, falsy]
        index = branch_index
      when "assign"
        # Top-level assignments mirror keys already loaded from Front Matter.
      else
        raise "Unsupported Liquid tag: #{token.value}"
      end
    elsif token.type == :output
      nodes << [:output, token.value]
    else
      nodes << [:text, token.value]
    end
    index += 1
  end
  [nodes, index, ""]
end

def lookup(path, env)
  parts = path.strip.split(".")
  value = env[parts.shift]
  parts.each do |part|
    value = if part == "size" && value.respond_to?(:size)
      value.size
    elsif value.is_a?(Hash)
      value[part]
    else
      value.respond_to?(part) ? value.public_send(part) : nil
    end
  end
  value
end

def condition_true?(expression, env)
  if (match = expression.match(/\A(.+?)\s*>\s*(\d+)\z/))
    lookup(match[1], env).to_i > match[2].to_i
  else
    value = lookup(expression, env)
    !value.nil? && value != false
  end
end

def render_output(expression, env)
  parts = expression.split("|").map(&:strip)
  value = lookup(parts.shift, env)
  parts.each do |filter|
    value = case filter
    when "escape" then CGI.escapeHTML(value.to_s)
    else raise "Unsupported Liquid filter: #{filter}"
    end
  end
  value.to_s
end

def render_nodes(nodes, env)
  nodes.map do |node|
    case node[0]
    when :text
      node[1]
    when :output
      render_output(node[1], env)
    when :for
      collection = lookup(node[2], env) || []
      collection.each_with_index.map do |item, index|
        child_env = env.merge(node[1] => item, "forloop" => {
          "index" => index + 1,
          "last" => index == collection.length - 1
        })
        render_nodes(node[3], child_env)
      end.join
    when :if, :unless
      result = condition_true?(node[1], env)
      result = !result if node[0] == :unless
      render_nodes(result ? node[2] : node[3], env)
    else
      raise "Unsupported node: #{node[0]}"
    end
  end.join
end

project_root = ARGV[2] ? File.expand_path(ARGV[2], Dir.pwd) : File.expand_path("..", __dir__)
source_path = ARGV[0] ? File.expand_path(ARGV[0], Dir.pwd) : File.join(project_root, "_source", "homepage.liquid")
output_path = ARGV[1] ? File.expand_path(ARGV[1], Dir.pwd) : File.join(project_root, "index.html")

source = File.read(source_path)
front_match = source.match(/\A---\n(.*?)\n---\n/m)
raise "Front Matter not found at the start of #{source_path}" unless front_match

data = YAML.load(front_match[1])
template = source[front_match.end(0)..]
tokens = tokenize(template)
nodes, final_index, = parse_nodes(tokens)
raise "Unparsed Liquid tokens remain" unless final_index == tokens.length

rendered = render_nodes(nodes, data).lstrip
rendered = rendered.gsub(/[ \t]+(?=\n|\z)/, "")
raise "Generated page does not start with <!DOCTYPE html>" unless rendered.match?(/\A<!DOCTYPE html>/i)
raise "Liquid marker remains in generated page" if rendered.include?("{{") || rendered.include?("{%")

generated_note = "  <!-- Generated from _source/homepage.liquid. Edit the source, then run: ruby scripts/build_homepage.rb -->\n"
rendered = rendered.sub(/\A(<!DOCTYPE html>\n)/i, "\\1#{generated_note}")

required_paths = [
  "images/yanqidai.jpg",
  "images/mountain-background.jpg",
  "images/mountain-background-mobile.jpg",
  "blogs/leetcode-hot100/index.html"
]
required_paths.each do |relative_path|
  raise "Generated page is missing #{relative_path}" unless rendered.include?(relative_path)
  raise "Repository file is missing: #{relative_path}" unless File.file?(File.join(project_root, relative_path))
end

FileUtils.mkdir_p(File.dirname(output_path))
temporary_path = "#{output_path}.tmp-#{Process.pid}"
begin
  File.write(temporary_path, rendered)
  File.rename(temporary_path, output_path)
ensure
  File.delete(temporary_path) if File.exist?(temporary_path)
end

puts "Generated #{output_path}"
puts "Content: #{data.fetch("papers").fetch("items").length} papers, #{data.fetch("experience").fetch("items").length} experiences, #{data.fetch("awards").fetch("items").length} awards, #{data.fetch("blogs").fetch("items").length} blogs"
