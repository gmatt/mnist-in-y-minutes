const JEKYLL_COMMENT_SELECTOR = ".highlight span.c1";

const highlightCodeOutput = () => {
    for (const node of document.querySelectorAll(JEKYLL_COMMENT_SELECTOR)) {
        if (node.textContent.startsWith(OUTPUT_MARKER)) {
            node.classList.add("output");
        } else if (node.textContent.startsWith(SHELL_COMMAND_MARKER)) {
            node.classList.add("shell-command");
        }
    }
};

highlightCodeOutput();
