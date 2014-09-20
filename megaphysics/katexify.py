import re
import execjs

singledollar = re.compile("(?<![\$])\$([^$]+)\$(?!\$)")
doubledollar = re.compile("\$\$([^$]+)\$\$")

katex = execjs.compile(open("assets/site_assets/js/katex.min.js").read().decode('utf-8'))


def eqn_to_html(latex_str):
    try:
        return katex.call("katex.renderToString", latex_str)
    except ReferenceError:
        print("Error rendering KaTeX HTML. Please ensure that you have")
        print("imported KaTeX into the Python namespace.")
        return False


def match_double_dollar(match):
    """ Converts $$<eqn>$$ to HTML """
    s = "\\displaystyle "+match.group(1)
    return "<div style='text-align: center;'>"+eqn_to_html(s)+"</div>"


def match_single_dollar(match):
    """ Converts $<eqn>$ to HTML """
    print(match.group(1))
    return eqn_to_html(match.group(1))


def katexify(content):
    content = re.sub(doubledollar, match_double_dollar, content)
    content = re.sub(singledollar, match_single_dollar, content)
    return content
