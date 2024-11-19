import type { CodeToHtmlOptions } from "@llm-ui/code";
import {
    allLangs,
    allLangsAlias,
    loadHighlighter,
    useCodeBlockToHtml,
} from "@llm-ui/code";

import parseHtml from "html-react-parser";
import { getSingletonHighlighterCore } from "shiki/core";
import { bundledLanguagesInfo } from "shiki/langs";
import { bundledThemes } from "shiki/themes";
import { type LLMOutputComponent } from "@llm-ui/react";
import { createOnigurumaEngine } from 'shiki/engine/oniguruma'

const highlighter = loadHighlighter(
    getSingletonHighlighterCore({
        langs: allLangs(bundledLanguagesInfo),
        langAlias: allLangsAlias(bundledLanguagesInfo),
        themes: Object.values(bundledThemes),
        engine: createOnigurumaEngine(() => import('shiki/wasm')),
    }),
);

const codeToHtmlOptions: CodeToHtmlOptions = {
    theme: "github-light",
};

// Customize this component with your own styling
const CodeBlock: LLMOutputComponent = ({ blockMatch }) => {
    const { html, code } = useCodeBlockToHtml({
        markdownCodeBlock: blockMatch.output,
        highlighter,
        codeToHtmlOptions,
    });
    if (!html) {
        // fallback to <pre> if Shiki is not loaded yet:
        return (
            <pre className="shiki">
                <code>{code}</code>
            </pre>
        );
    }
    return <>{parseHtml(html)}</>;
};

export default CodeBlock;