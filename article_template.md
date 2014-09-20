title: A Guide To Article Writing
course: MegaPhysics
author: Harry Maclean

Writing Articles
================

Set Up
------
New articles should be created in the articles directory. Name the article something sensible, and if it is
part of a course, number it accordingly (e.g. the first article in a mechanics course would be mechanics-1.md).
Use the extension .md, which indicates that the file is a Markdown file.
DO NOT put spaces in your filename.
This will mess up the directory structure and probably other things as well.

Markdown is a simple markup language intended to be human-readable.
Most of the rules of Markdown should be obvious once you've seen them, and the others are easy to remember.

Headings
--------

Main headings are created by underlining them with equals signs (=)
Sub headings are underlined with hyphens (-)

Writing
---------

The style of writing you choose may depend on the audience you're addressing.
Articles aimed at those with no Physics or Maths skills should avoid equations and complex diagrams,
whereas the more advanced articles can be more technical and mathsy. Don't go overboard though - 
full derivations of everything would result in pages of equations that become very unreadable.
This is a mistake that a lot of textbooks make that we try to avoid.

Put each sentence on a new line to make reviewing easier.
You can also split a sentence across two lines if it gets too long.
In the build system we try to stick to 80 characters per line but this rule isn't particularly
important for articles so don't worry if you don't stick to it.
Markdown will combine consecutive lines into one contiguous paragraph.
If you want to start a new paragraph, leave a blank line.

*Italic* text is wrapped in asterisks.
**Bold** text is wrapped in double asterisks.
_Underlined_ text is wrapped in underscores.

Lists
-----
An unorderd (bullet point) list is written as:
  - One thing
  - A different thing
  - An auxillary thing

Numbered lists are written as
  1. Break eggs into bowl
  2. Whisk
  3. Season
  4. Add to frying pan
  5. Cook on moderate heat
  6. Fold and serve

Tables
------
Simple tables can be created as follows:

| Quark   | Charge |
| ------- | ------:|
| Up      | + 2/3  |
| Top     | + 2/3  |
| Charm   | + 2/3  |
| Down    | - 1/3  |
| Bottom  | - 1/3  |
| Strange | - 1/3  |

More complicated tables might require html markup - see the particle physics article for an example.

Links
-----

Similar to Wikipedia, we can link to other pages on the site to allow readers to explore
topics further.
The text of the link should be similar to or the same as the title of the 
page you are linking to.

A link is created as follows:
[Quarks](quark-1)

The text in square brackets is what the user will see as the link text, and the text in round brackets
is the name of the file that you wish to link to, without the file extension. All articles on the site are
in the articles directory, so to link to page, find which file it is (you can see this on the end of the URL on the site)
and enter it in the round brackets without the .md/.html extension.

If you want to link to another website, you can use the same syntax, e.g.

[Wikipedia](en.wikipedia.org)

If the text in round brackets isn't the name of an article, the build system will assume it is a link to an external website
and treat it as such. Try to avoid linking to external websites unless necessary - users should ideally be able to learn everything
they need to on the MegaPhysics site.

Images
------

To add an image to an article, first place it in the following directory:

assets/article_assets/[article filenname]/images

Where [article filename] is the filename of your article (without the file extension, so atom-1.md would have an assets directory called atom-1)
If the directory doesn't exist then you should create it.
Make sure that the directory name is exactly the same as your article filename, minus the extension.

You can use any image format that the web supports, so one of:
  - JPEG
  - PNG
  - GIF

GIFs can of course be animated, so this is an easy way to put animations in your article.

Please make sure all your images are either your own creation or are licensed to allow reuse.
It's nicer if images are created specifically for the site so they fit the overall style etc.

LaTeX
-----

You can add LaTeX equations to your article by enclosing them in single dollar signs for inline equations and double dollar signs for equations
that appear on their own line. For example, $F = ma$ is an inline equation and $$V = IR$$ is an equation on its own line.

Scripts
-------

You probably won't need this, but if you want to put custom javascript on your page, place the javascript file in 

assets/article_assets/[article filename]/scripts

and then just add an HTML script tag in your article where you want to load the script. For example:

<script type="text/javascript" src="assets/article_assets/atom-1/some_script.js"></script>

More Info
---------

Markdown is massively popular, so if you're not sure about something just give it a google and you'll get tons of tutorials etc.
