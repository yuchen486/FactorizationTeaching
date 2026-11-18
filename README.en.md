# Factorization in Ten Minutes

[中文](README.md) · [Live site](https://yuchen486.github.io/FactorizationTeaching/)

![Overview of the Factorization in Ten Minutes static site](assets/pages-overview.png)

A complete teaching-resource package for a mathematics-teaching methods course. Based on section 8.4 of the current Huaibei reference edition of the Shanghai Science and Technology Press Grade 7 mathematics textbook, it presents a 600-second micro-teaching lesson on introductory factorization by extracting a common factor.

## Start here

- Visit the [GitHub Pages site](https://yuchen486.github.io/FactorizationTeaching/)
- For offline use, open [docs/index.html](docs/index.html) directly; no build step or backend is required
- Review the [source and verification notes](references/sources.md)

|Resource|Editable source|Reading or presentation entry|
|---|---|---|
|Teaching script|[Markdown](lesson-plans/L01-script.md)|[Printable reader](docs/script.html)|
|Lesson plan|[Plan](lesson-plans/L01-lesson-plan.md)|[Printable reader](docs/lesson.html)|
|Board design|[SVG](board-design/L01-board.svg)|[Step-by-step board](docs/board.html)|
|Slides|[Storyboard](slides/L01-storyboard.md), [copy and illustration plan](slides/L01-api-v3.json)|[HTML slides](docs/slides.html), [PPTX](outputs/L01-课件.pptx)|
|Exercises|[Questions and answers](exercises/L01-exercises.md)|E01–E05 in-class, E06 after-class|

## Repository layout

- `docs/`: static site deployed to GitHub Pages
- `lesson-plans/`, `board-design/`, `slides/`, and `exercises/`: teaching materials and editable sources
- `assets/` and `outputs/`: slide images and accepted deliverables
- `scripts/`: content-build and verification scripts; `work/` is ignored local scratch space

Student responses are scripted examples, and the actual lesson duration should be confirmed through rehearsal. The textbook is referenced only for teaching scope and structure; this repository does not include a full textbook.

## Attribution and license

Original author: [HNNUYUXUAN / Yuxuan Miao](https://github.com/HNNUYUXUAN). The public repository is maintained by [yuchen486](https://github.com/yuchen486).

This repository is released under [CC BY-NC-SA 4.0](LICENSE). Reuse and adaptations require attribution, are limited to non-commercial use, and must be shared under the same terms.
