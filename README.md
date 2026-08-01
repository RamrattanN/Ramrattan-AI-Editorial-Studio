# Ramrattan AI Editorial Studio

> **Engineering AI-assisted thought leadership with the discipline of
> software development.**

Ramrattan AI Editorial Studio is an adaptive editorial partner that
helps Authors transform evolving ideas, evidence, expertise, and
perspective into publication-ready thought leadership.

**The Studio adapts to the Author's creative process - never the other
way around.**

## Authors May Begin With

- a URL,
- a headline,
- a topic,
- something seen in the news,
- a personal observation,
- a developed perspective,
- rough notes,
- a draft,
- or any useful combination.

The Studio interprets what is happening before imposing structure.

## Core Commitments

- Infer before asking.
- Preserve creative momentum.
- Treat perspective as a first-class input.
- Keep every editorial decision revisable.
- Preserve useful context across changes.
- Use evidence to strengthen thinking.
- Explain significant recommendations.
- Synthesize rather than imitate.
- Optimize for quality rather than content volume.

## Initial Publishing Module

The first production module focuses on LinkedIn:

- thought-leadership articles,
- seven-slide carousels,
- hero infographics,
- headlines and hooks,
- evidence-supported insights,
- practical takeaways,
- calls to action,
- attribution,
- hashtags,
- and LinkedIn descriptions.

LinkedIn is the first channel, not the permanent boundary.

## Product Documentation

1. [PRD v1.0](docs/product/PRD_v1.0.md)
2. [Product Constitution](docs/product/Constitution.md)
3. [Product Principles](docs/product/Product_Principles.md)
4. [Studio Contract](docs/product/Studio_Contract.md)
5. [Adaptive Editorial Model](docs/product/Adaptive_Editorial_Model.md)
6. [Author Journey](docs/product/Author_Journey.md)
7. [Things We Will Not Do](docs/product/Things_We_Will_Not_Do.md)
8. [Glossary](docs/product/Glossary.md)
9. [Decision Log](docs/product/Decision_Log.md)
10. [Editorial Intelligence Manifesto](docs/product/Editorial_Intelligence_Manifesto.md)

## Architecture Status

The current `studio.workflow` package remains an engineering prototype.

The target architecture is an adaptive Editorial Context model.

## Validation

```bash
python3 -m compileall -q studio tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

## License

This project is licensed under the MIT License.

---

The Author owns the idea. The Studio helps make it stronger.
