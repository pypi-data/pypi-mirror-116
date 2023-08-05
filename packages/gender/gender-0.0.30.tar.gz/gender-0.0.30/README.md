# gender
Have a name and possibly an email address and wondering whether it’s a male or a female? This package gives you the answer.

### Key Advantages

* Very simple to use
* Relies on a dataset of 216,000+ unique names
* Covers [hypocorisms](https://en.wikipedia.org/wiki/Hypocorism) (English only at this time)
* Makes use of a person’s email address (if available) via searching for names and [grammatical gender](https://en.wikipedia.org/wiki/Grammatical_gender) words in the prefix
* Doesn’t care if the input has bad formatting

### Latest Update (11/08/2021)

* male names: 93,307 
* female names: 121,087 
* unisex names: 2,412
* total names: 216,806

### Installation
`pip3 install gender`

### Quickstart

```
from gender import GenderDetector
gd = GenderDetector()
gd.get_gender('jeroen van dijk')
```
which gives you
```
Person(title=None, first_name='jeroen', last_name='van dijk', email=None, gender='m')
```