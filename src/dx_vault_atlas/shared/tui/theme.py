"""Theme management for TUI applications.

Supports Catppuccin color palettes with dynamic theme switching.
"""

from typing import ClassVar

# Catppuccin Theme Palettes
THEMES: dict[str, dict[str, str]] = {
    "mocha": {
        "crust": "#11111b",
        "mantle": "#181825",
        "base": "#1e1e2e",
        "surface0": "#313244",
        "surface1": "#45475a",
        "surface2": "#585b70",
        "overlay0": "#6c7086",
        "overlay1": "#7f849c",
        "overlay2": "#9399b2",
        "subtext0": "#a6adc8",
        "subtext1": "#bac2de",
        "text": "#cdd6f4",
        "lavender": "#b4befe",
        "blue": "#89b4fa",
        "sapphire": "#74c7ec",
        "sky": "#89dceb",
        "teal": "#94e2d5",
        "green": "#a6e3a1",
        "yellow": "#f9e2af",
        "peach": "#fab387",
        "maroon": "#eba0ac",
        "red": "#f38ba8",
        "mauve": "#cba6f7",
        "pink": "#f5c2e7",
        "flamingo": "#f2cdcd",
        "rosewater": "#f5e0dc",
    },
    "latte": {
        "crust": "#dce0e8",
        "mantle": "#e6e9ef",
        "base": "#eff1f5",
        "surface0": "#ccd0da",
        "surface1": "#bcc0cc",
        "surface2": "#acb0be",
        "overlay0": "#9ca0b0",
        "overlay1": "#8c8fa1",
        "overlay2": "#7c7f93",
        "subtext0": "#6c6f85",
        "subtext1": "#5c5f77",
        "text": "#4c4f69",
        "lavender": "#7287fd",
        "blue": "#1e66f5",
        "sapphire": "#209fb5",
        "sky": "#04a5e5",
        "teal": "#179299",
        "green": "#40a02b",
        "yellow": "#df8e1d",
        "peach": "#fe640b",
        "maroon": "#e64553",
        "red": "#d20f39",
        "mauve": "#8839ef",
        "pink": "#ea76cb",
        "flamingo": "#dd7878",
        "rosewater": "#dc8a78",
    },
    "frappe": {
        "crust": "#232634",
        "mantle": "#292c3c",
        "base": "#303446",
        "surface0": "#414559",
        "surface1": "#51576d",
        "surface2": "#626880",
        "overlay0": "#737994",
        "overlay1": "#838ba7",
        "overlay2": "#949cbb",
        "subtext0": "#a5adce",
        "subtext1": "#b5bfe2",
        "text": "#c6d0f5",
        "lavender": "#babbf1",
        "blue": "#8caaee",
        "sapphire": "#85c1dc",
        "sky": "#99d1db",
        "teal": "#81c8be",
        "green": "#a6d189",
        "yellow": "#e5c890",
        "peach": "#ef9f76",
        "maroon": "#ea999c",
        "red": "#e78284",
        "mauve": "#ca9ee6",
        "pink": "#f4b8e4",
        "flamingo": "#eebebe",
        "rosewater": "#f2d5cf",
    },
    "macchiato": {
        "crust": "#181926",
        "mantle": "#1e2030",
        "base": "#24273a",
        "surface0": "#363a4f",
        "surface1": "#494d64",
        "surface2": "#5b6078",
        "overlay0": "#6e738d",
        "overlay1": "#8087a2",
        "overlay2": "#939ab7",
        "subtext0": "#a5adcb",
        "subtext1": "#b8c0e0",
        "text": "#cad3f5",
        "lavender": "#b7bdf8",
        "blue": "#8aadf4",
        "sapphire": "#7dc4e4",
        "sky": "#91d7e3",
        "teal": "#8bd5ca",
        "green": "#a6da95",
        "yellow": "#eed49f",
        "peach": "#f5a97f",
        "maroon": "#ee99a0",
        "red": "#ed8796",
        "mauve": "#c6a0f6",
        "pink": "#f5bde6",
        "flamingo": "#f0c6c6",
        "rosewater": "#f4dbd6",
    },
}

THEME_ORDER = ["mocha", "latte", "frappe", "macchiato"]


class ThemeManager:
    """Manages theme state and CSS generation.

    Provides dynamic CSS generation based on the current theme and
    supports cycling through available Catppuccin variants.
    """

    current_theme: ClassVar[str] = "mocha"

    @classmethod
    def get_colors(cls) -> dict[str, str]:
        """Get colors for the current theme."""
        return THEMES[cls.current_theme]

    @classmethod
    def cycle_theme(cls) -> str:
        """Cycle to the next theme and return its name."""
        current_idx = THEME_ORDER.index(cls.current_theme)
        next_idx = (current_idx + 1) % len(THEME_ORDER)
        cls.current_theme = THEME_ORDER[next_idx]
        return cls.current_theme

    @classmethod
    def get_css(cls) -> str:
        """Generate CSS for the current theme."""
        c = cls.get_colors()
        return f"""
Screen {{
    background: {c["base"]};
}}

#header-panel {{
    dock: top;
    height: 3;
    padding: 0 2;
    background: {c["surface0"]};
    border-bottom: solid {c["surface1"]};
}}

#header-title {{
    width: 100%;
    height: 1;
    margin-top: 1;
    text-align: center;
    color: {c["blue"]};
    text-style: bold;
}}

Footer {{
    background: {c["surface0"]};
}}

#wizard {{
    height: auto;
    padding: 1 2;
}}

#wizard.maximized {{
    height: 1fr;
    min-height: 100%;
}}

.step-done {{
    height: 1;
    color: {c["subtext0"]};
}}

.prompt-label {{
    color: {c["text"]};
    margin-bottom: 0;
}}

.stats {{
    margin-bottom: 1;
    color: {c["text"]};
}}

.file-header {{
    color: {c["blue"]};
    text-style: bold;
    margin-top: 1;
}}

.missing-info {{
    color: {c["yellow"]};
}}

.preview-box {{
    border: tall {c["surface1"]};
    padding: 1;
    max-height: 8;
    background: {c["surface0"]};
}}

Input {{
    border: tall {c["surface1"]};
    background: {c["surface0"]};
}}

Input:focus {{
    border: tall {c["blue"]};
}}

OptionList, VimOptionList {{
    height: auto;
    max-height: 10;
    background: transparent;
    border: none;
    padding: 0;
}}

OptionList > .option-list--option,
VimOptionList > .option-list--option {{
    padding: 0 1;
}}

OptionList > .option-list--option-highlighted,
VimOptionList > .option-list--option-highlighted {{
    background: {c["surface1"]};
    color: {c["blue"]};
    text-style: bold;
}}

.success {{
    margin-top: 1;
    color: {c["green"]};
    text-style: bold;
}}

.path {{
    color: {c["overlay0"]};
}}

.hint {{
    margin-top: 1;
    color: {c["overlay0"]};
}}

.result-container {{
    padding: 2;
}}

.success-title {{
    margin-bottom: 1;
}}

.path-display {{
    margin-bottom: 1;
}}

.theme-indicator {{
    dock: right;
    width: auto;
    padding: 0 1;
    color: {c["overlay1"]};
}}
"""


# For backwards compatibility - static CSS using default theme
SHARED_CSS = ThemeManager.get_css()
