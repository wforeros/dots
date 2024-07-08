-- Keymaps are automatically loaded on the VeryLazy event
-- jlsdkfjsdfjklsdjflk
-- jklsfjsdlfjdskfjklsdf
-- jsklfjsdjflk
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- Map Ctrl+b in insert mode to delete to the end of the word without leaving insert mode
vim.keymap.set("i", "<C-b>", "<C-o>de")
vim.keymap.set("i", "<C-r>", "<Esc><c-r><Esc>i", { silent = true })
vim.keymap.set("i", "<C-d>", "<Esc>u<Esc>i", { silent = true })
vim.keymap.set("i", "<C-Space>", 'copilot#Accept("\\<CR>")', {
  expr = true,
  replace_keycodes = false,
})

vim.g.copilot_no_tab_map = false
vim.keymap.set("n", "<CapsLock>", "<Ctrl>", { silent = true })

vim.keymap.set("n", "[h", ":GitGutterPrevHunk <CR>", { desc = "Jump to the previous git hunk" })
vim.keymap.set("n", "]h", ":GitGutterNextHunk <CR>", { desc = "Jump to the next git hunk" })
