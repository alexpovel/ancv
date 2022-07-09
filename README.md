# ancv

Getting you [an CV](https://www.youtube.com/watch?v=mJUtMEJdvqM) (ANSI-v?) straight to your terminal.

Be warned though, this is entirely useless:

![Users Venn diagram](docs/users-venn.svg)

## Getting started

1. Create a resume according to the [JSON Resume Schema](https://jsonresume.org/schema/) ([schema specification](https://github.com/jsonresume/resume-schema/blob/master/schema.json)) either:

   - manually,
   - exporting from LinkedIn using [Joshua Tzucker's LinkedIn exporter](https://joshuatz.com/projects/web-stuff/linkedin-profile-to-json-resume-exporter/) ([repo](https://github.com/joshuatz/linkedin-to-jsonresume)), or
   - exporting from one of the platforms advertised as offering [JSON resume integration](https://jsonresume.org/schema/):
     - <https://gitconnected.com/portfolio-api>
     - <https://represent.io/>
     - <https://www.doyoubuzz.com/us/>
2. [Create a gist](https://gist.github.com/) named `resume.json` with those resume contents.
   See [here](https://gist.github.com/thomasdavis/c9dcfa1b37dec07fb2ee7f36d7278105) for a working example from a [JSON Resume co-founder](https://github.com/orgs/jsonresume/people).
3. Try it out!

   ```bash
   curl -L ancv.io/username
   ```

## Concept

(put this as an SVG flowchart, left to right with conceptual sketches)

Skeleton + Theme + Language + ASCII-mode toggle + Resume Data ==> terminal CV

## TODO

- [ ] Core application
  - [ ] 3 full templates implemented
  - [ ] ASCII-safe mode implemented
- [ ] Implement test suite
  - [ ] Unit tests (not many to do...)
  - [ ] Integration tests:
    - [ ] Create *one* fully featured JSON resume
    - [ ] Create derived resumes with all possible fields (all combinations thereof?) set to `None` where legal (given the schema)
    - [ ] Compare all these to expected files (the files contain the ANSI escape characters literally)
  - [ ] [Load tests](https://molotov.readthedocs.io/en/stable/index.html)
- [ ] Other
  - [ ] ~~<https://ancv.io> landing page for browsers~~ (just a redirect to GitHub for now)
  - [x] Venn diagram
    - [x] ~~[Hand- [ ]draw](https://www.youtube.com/watch?v=iN1MsCXkPSA) on ReMarkable?~~
    - [x] One circle: 'people working with resumes'
    - [x] other circle: 'people working with terminals'
    - [x] *tiny* overlap: 'you', with arrow
  - [ ] Demos
    - [ ] `curl`, `wget` (PowerShell?) examples
    - [ ] all templates
      - [ ] all languages

## Roadmap

- [ ] Multiple `locale` support for hardcoded strings (like `Present` for a missing end date)
  - [ ] German, French, Spanish
- [ ] Image support (fetch bitmap, convert to ASCII art ([random example](https://gist.github.com/mayjs/5dc934d42bad05825ea9cd5a26517d97)))

## Other solutions

Very hard to find any, and even hard to google.
For example, `bash curl curriculum vitae` will prompt Google to interpret `curriculum vitae == resume`, which isn't wrong but `curl resume` is an entirely unrelated query (concerned with resuming halted downloads and such).

- <https://github.com/soulshake/cv.soulshake.net>

Related, but 'fake' hits:

- <https://ostechnix.com/create-beautiful-resumes-commandline-linux/>
