# Scattertext 0.0.2.1
A tool for finding distinguishing terms in small-to-medium-sized
corpora, and presenting them in a sexy, interactive scatter plot with 
non-overlapping term labels.  Exploratory data analysis just 
got more fun.



## Installation

`$ pip install scattertext && python -m spacy.en.download`

## Changelog
### 0.0.2.1.1

Addition of `strip_final_period` param to `FeatsFromSpacyDoc` to deal with spaCy 
 tokenization of all-caps documents that can leave periods at the end of terms.

### 0.0.2.1.0

I've added support for Chinese, including the ChineseNLP class, which uses a RegExp-based 
sentence splitter and [Jieba](https://github.com/fxsjy/jieba) for word 
segmentation. To use it, see the `demo_chinese.py` file.  Note that `CorpusFromPandas`
currently does not support ChineseNLP.

In order for the visualization to work, set the `chinese_mode` flat to `True` in
`produce_scattertext_explorer`.

## Overview
 
This is a tool that's intended for visualizing what words and phrases
 are more characteristic of a category than others.  
 
Consider this example: 

[![Conventions-Visualization.html](https://jasonkessler.github.io/2012Conventions.png)](https://jasonkessler.github.io/Conventions-Visualization.html)

Looking at this seem overwhelming.  In fact, it's a relatively simple visualization of word use 
during the 2012 political convention.  Each dot corresponds to a word or phrase mentioned by Republicans or Democrats
during their conventions.  The closer a dot is to the top of the plot, the more frequently it was used by 
Democrats.  The further right a  dot, the more that word or phrase was used by Republicans.  Words frequently
used by both parties, like "of" and "the" and even "Mitt" tend to occur in the upper-right-hand corner. Although very low 
frequency words have been hidden to preserve computing resources, a word that neither party used, like "giraffe" 
 would be in the bottom-left-hand corner.  
 
The interesting things happen close to the upper-left and lower-right corners.  In the upper-left corner, 
words like "auto" (as in auto bailout) and "millionaires" are frequently used by Democrats but infrequently or never used 
by Republicans.  Likewise, terms frequently used by Republicans and infrequently by Democrats occupy the
 bottom-right corner.  These include "big government" and "olympics", referring to the Salt Lake City Olympics in which 
 Gov. Romney was involved.
 
Terms are colored by their association.  Those that are more associated with Democrats are blue, and those 
more associated with Republicans red.  
   
The inspiration for this visualization came from Dataclysm (Rudder, 2014).
  
Scattertext is designed to help you build these graphs and efficiently label points on them. 

The documentation (including this readme) is a work in 
progress.  Please see the quickstart as well as the accompanying Juypter 
notebooks, and poking around the code and tests should give you a good idea of how things work. 

The library covers some novel and effective term-importance formulas, including **Scaled F-Score**.  See slides [52](http://www.slideshare.net/JasonKessler/turning-unstructured-content-into-kernels-of-ideas/52) to [59](http://www.slideshare.net/JasonKessler/turning-unstructured-content-into-kernels-of-ideas/59) of the [Turning Unstructured Content into Kernels of Ideas](http://www.slideshare.net/JasonKessler/turning-unstructured-content-into-kernels-of-ideas/) talk for more details.   

## Examples 

I recommend you start with this example first.  It explains some design decisions that were made in 
Scattertext, and explains the strings of points.  You can 
find it [2012 Political Convention Exploration](http://bit.ly/scattertextdevelopment).

Scattertext can also be used to visualize **topic models**, analyze how **word vectors** and categories interact, and understand **document classification models**.  You can see examples of all of these applied to [2016 Presidential Debate transcripts](https://bit.ly/scattertext2016debates).     

Finally, we use the task of predicting a movie's revenue from the content of its reviews as an example of 
tuning Scattertext. See the analysis at [Movie Reviews and Revenue](http://bit.ly/scattertextrevenuemovie). 

## Quickstart

The following code creates a stand-alone HTML file that analyzes words 
used by Democrats and Republicans in the 2012 party conventions, and outputs some notable
 term associations.
 
First, import Scattertext and spaCy.

```pydocstring
>>> import scattertext as st
>>> import spacy
>>> from pprint import pprint
```

Next, assemble the data you want to analyze into a Pandas data frame. It should have
at least two columns, the text you'd like to analyze, and the category you'd like to 
study. Here, the `text` column contains convention speeches while the `party` column
 contains the party of the speaker.  We'll eventually use the `speaker` column
 to label snippets in the visualization.

```pydocstring
>>> convention_df = st.SampleCorpora.ConventionData2012.get_data()  
>>> convention_df.iloc[0]
party                                               democrat
speaker                                         BARACK OBAMA
text       Thank you. Thank you. Thank you. Thank you so ...
Name: 0, dtype: object
```

Turn the data frame into a Scattertext Corpus to begin analyzing it.  To look for differences 
in parties, set the `category_col` parameter to `'party'`, and use the speeches, 
present in the `text` column, as the texts to analyze by setting the `text` col 
parameter.  Finally, pass a spaCy model in to the `nlp` argument and call `build()` to construct the corpus.
 
```pydocstring
# Turn it into a Scattertext Corpus 
>>> nlp = spacy.en.English()
>>> corpus = st.CorpusFromPandas(convention_df, 
...                              category_col='party', 
...                              text_col='text',
...                              nlp=nlp).build()
```

Let's see characteristic terms in the corpus, and terms that are most associated Democrats and Republicans.  See slides [52](http://www.slideshare.net/JasonKessler/turning-unstructured-content-into-kernels-of-ideas/52) to [59](http://www.slideshare.net/JasonKessler/turning-unstructured-content-into-kernels-of-ideas/59) of the [Turning Unstructured Content ot Kernels of Ideas](http://www.slideshare.net/JasonKessler/turning-unstructured-content-into-kernels-of-ideas/) talk for more details on these approaches. 

Here are the terms that differentiate the corpus from a general English corpus. 
```pydocstring
>>> print(list(corpus.get_scaled_f_scores_vs_background().index[:10]))
['obama',
 'romney',
 'barack',
 'mitt',
 'obamacare',
 'biden',
 'romneys',
 'hardworking',
 'bailouts',
 'autoworkers']
```

Here are the terms that are most associated with Democrats: 

```pydocstring
>>> term_freq_df = corpus.get_term_freq_df()
>>> term_freq_df['Democratic Score'] = \
...  corpus.get_scaled_f_scores('democrat')
>>> pprint(list(term_freq_df.sort_values(by='Democratic Score', 
...                                      ascending=False).index[:10]))
['auto',
 'america forward',
 'auto industry',
 'insurance companies',
 'pell',
 'last week',
 'pell grants',
 "women 's",
 'platform',
 'millionaires']
```

And Republicans:
```pydocstring
>>> term_freq_df['Republican Score'] = \
...  corpus.get_scaled_f_scores('republican')
>>> pprint(list(term_freq_df.sort_values(by='Democratic Score', 
...                                      ascending=False).index[:10]))
['big government',
 "n't build",
 'mitt was',
 'the constitution',
 'he wanted',
 'hands that',
 'of mitt',
 '16 trillion',
 'turned around',
 'in florida']
```

Now, let's write the scatter plot a stand-alone HTML file.  We'll make the y-axis category  "democrat", and name
the category "Democrat" with a capital "D" for presentation 
purposes.  We'll name the other category "Republican" with a capital R.  All documents in the corpus without 
the category "democrat" will be considered Republican. We set the width of the visualization in pixels, and label 
each excerpt with the speaker using the `metadata` parameter.  Finally, we write the visualization to an HTML file.
 
```pydocstring
>>> html = st.produce_scattertext_explorer(corpus,
...          category='democrat',
...          category_name='Democratic',
...          not_category_name='Republican',
...          width_in_pixels=1000,
...          metadata=convention_df['speaker'])
>>> open("Convention-Visualization.html", 'wb').write(html.encode('utf-8'))
```
Below is what the webpage looks like.  Click it and wait a few minutes for the interactive version.
[![Conventions-Visualization.html](https://jasonkessler.github.io/2012Conventions.png)](https://jasonkessler.github.io/Conventions-Visualization.html)

## A note on chart layout

[Cozy: The Collection Synthesizer](https://github.com/uwplse/cozy) (Loncaric, 2016) was used to help determine 
which terms could be labeled without overlapping a circle or another label.  It automatically built a data structure to efficiently store and query the locations of each circle and labeled term.

The script to build `rectangle-holder.js` was
```
fields ax1 : long, ay1 : long, ax2 : long, ay2 : long
assume ax1 < ax2 and ay1 < ay2
query findMatchingRectangles(bx1 : long, by1 : long, bx2 : long, by2 : long)
    assume bx1 < bx2 and by1 < by2
    ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1(py2)
```


## Data Day Texas 2017 Presentation

[Scattertext: A Tool for Visualizing Differences in Language
](http://www.slideshare.net/JasonKessler/scattertext-a-tool-for-visualizing-differences-in-language)

## Technical underpinnings

Please see [Turning Unstructured Content into Kernels of Ideas](https://www.slideshare.net/JasonKessler/turning-unstructured-content-into-kernels-of-ideas) for an introduction to the metrics and algorithms used.

## Sources
* 2012 Convention Data: scraped from [The New York Times.](http://www.nytimes.com/interactive/2012/09/06/us/politics/convention-word-counts.html?_r=0)
* count_1w: Peter Norvig assembled this file (downloaded from [norvig.com](http://norvig.com/ngrams/count_1w.txt)). See http://norvig.com/ngrams/ for an explanation of how it was gathered from a very large corpus.
* hamlet.txt: William Shakespeare. From [shapespeare.mit.edu](http://shakespeare.mit.edu/hamlet/full.html)
* Inspiration for text scatter plots: Rudder, Christian. Dataclysm: Who We Are (When We Think No One's Looking). Random House Incorporated, 2014.
* The efficient RectangleHolder Javascript data structure was automatically generated using [Cozy: The Collection Synthesizer](https://github.com/uwplse/cozy).   Loncaric, Calvin. "Cozy: synthesizing collection data structures." Proceedings of the 2016 24th ACM SIGSOFT International Symposium on Foundations of Software Engineering. ACM, 2016.
* Loncaric, Calvin. "Cozy: synthesizing collection data structures." Proceedings of the 2016 24th ACM SIGSOFT International Symposium on Foundations of Software Engineering. ACM, 2016.
 