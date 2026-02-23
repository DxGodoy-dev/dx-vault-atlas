"""Tests for shared TUI widgets."""

from dx_vault_atlas.services.note_creator.models.enums import NoteTemplate, Priority
from dx_vault_atlas.shared.tui.widgets import (
    VimOptionList,
    create_enum_options,
    create_vim_option_list,
)


class TestCreateEnumOptions:
    """Tests for create_enum_options helper."""

    def test_creates_options_from_string_enum(self) -> None:
        """String enum values are formatted as title case."""
        options, default = create_enum_options(NoteTemplate, 0, "template")

        assert len(options) == len(NoteTemplate)
        assert default == 0
        # First option should have (default) marker
        assert "(default)" in str(options[0].prompt)

    def test_creates_options_from_int_enum(self) -> None:
        """Int enum values show name and value."""
        options, default = create_enum_options(Priority, 1, "priority")

        assert len(options) == len(Priority)
        assert default == 1
        # Should show format like "Medium (2)"
        assert "(" in str(options[0].prompt)

    def test_option_ids_have_correct_format(self) -> None:
        """Option IDs should be prefix-index format."""
        options, _ = create_enum_options(NoteTemplate, 0, "template")

        assert options[0].id == "template-0"
        assert options[1].id == "template-1"


class TestCreateVimOptionList:
    """Tests for create_vim_option_list helper."""

    def test_creates_vim_option_list(self) -> None:
        """Creates VimOptionList with correct options."""
        opt_list = create_vim_option_list(NoteTemplate, 0, "template")

        assert isinstance(opt_list, VimOptionList)
        assert opt_list.id == "template-options"
        assert opt_list.highlighted == 0

    def test_default_highlighted(self) -> None:
        """Default option is highlighted."""
        opt_list = create_vim_option_list(Priority, 2, "priority")

        assert opt_list.highlighted == 2


class TestVimOptionList:
    """Tests for VimOptionList widget."""

    def test_has_vim_bindings(self) -> None:
        """VimOptionList has j/k bindings."""
        bindings = {b.key for b in VimOptionList.BINDINGS}

        assert "j" in bindings
        assert "k" in bindings
        assert "down" in bindings
        assert "up" in bindings
        assert "enter" in bindings
        assert "space" in bindings
