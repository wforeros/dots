-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
--

-- Map Ctrl+b in insert mode to delete to the end of the word without leaving insert mode
vim.keymap.set("i", "jj", "<esc>")
vim.keymap.set("i", "<C-b>", "<C-o>de")
vim.keymap.set("i", "<c-r>", "<esc><c-r><esc>i", { silent = true })
vim.keymap.set("i", "<C-d>", "<Esc>u<Esc>i", { silent = true })
vim.keymap.set("i", "<C-Space>", 'copilot#Accept("\\<CR>")', {
  expr = true,
  replace_keycodes = false,
})

vim.g.copilot_no_tab_map = false
vim.keymap.set("n", "<CapsLock>", "<Ctrl>", { silent = true })

vim.keymap.set("n", "[h", ":GitGutterPrevHunk <CR>", { desc = "Jump to the previous git hunk" })
vim.keymap.set("n", "]h", ":GitGutterNextHunk <CR>", { desc = "Jump to the next git hunk" })

vim.keymap.set("n", "<leader>fw", ":Neotree float<CR>", { desc = "Open neotree floating" })

vim.keymap.set("n", "-", require("oil").open, { desc = "Open parent directory" })

-- Obsidian
vim.keymap.set("n", "<leader>o", "", { desc = "Open Obsidian menu" })
vim.keymap.set("n", "<leader>on", ":ObsidianNewFromTemplate<CR>", { desc = "New Obsidian note" })
vim.keymap.set("n", "<leader>oo", ":ObsidianOpen<CR>", { desc = "Open Obsidian note using Obsidian" })
vim.keymap.set("n", "<leader>os", ":ObsidianSearch<CR>", { desc = "Search Obsidian notes" })
vim.keymap.set("n", "<leader>ot", ":ObsidianTags<CR>", { desc = "List Obsidian tags" })
vim.keymap.set("n", "<leader>of", ":ObsidianFollow<CR>", { desc = "Follow Obsidian link" })
vim.keymap.set("n", "<leader>op", ":ObsidianPasteImage<CR>", { desc = "Paste image into Obsidian" })
vim.keymap.set("n", "<leader>or", ":ObsidianRename<CR>", { desc = "Rename Obsidian note" })

-- Obsidian Links
vim.keymap.set("n", "<leader>ol", "", { desc = "Open Obsidian links menu" })
vim.keymap.set("n", "<leader>olo", ":ObsidianFollowLink<CR>", { desc = "Open link under cursor" })
vim.keymap.set("n", "<leader>oll", ":ObsidianLinks<CR>", { desc = "List Obsidian links in this file" })

-- Obsidian Dily
vim.keymap.set("n", "<leader>od", "", { desc = "Open Obsidian Daily menu" })
vim.keymap.set("n", "<leader>odt", ":ObsidianToday<CR>", { desc = "Open today note" })
vim.keymap.set("n", "<leader>odl", ":ObsidianDailies<CR>", { desc = "List dailies" })

-- Obsidian Isert
vim.keymap.set("n", "<leader>oi", "", { desc = "Open Obsidian insert menu" })
vim.keymap.set("n", "<leader>oit", ":ObsidianTemplate<CR>", { desc = "Insert Obsidian template on current note" })

-- Rename
vim.keymap.set("n", "<leader>rn", ":IncRename ")

-- Buffers
vim.keymap.set("n", "<leader>n", "<cmd>:bd<CR>", { desc = "Close buffer" })

local M = {}

local ls = require("luasnip")
function M.expand_or_jump()
  if ls.expand_or_jumpable() then
    ls.expand_or_jump()
  end
end

function M.jump_next()
  if ls.jumpable(1) then
    ls.jump(1)
  end
end

function M.jump_prev()
  if ls.jumpable(-1) then
    ls.jump(-1)
  end
end

function M.change_choice()
  if ls.choice_active() then
    ls.change_choice(1)
  end
end

function M.reload_package(package_name)
  for module_name, _ in pairs(package.loaded) do
    if string.find(module_name, "^" .. package_name) then
      package.loaded[module_name] = nil
      require(module_name)
    end
  end
end

function M.refresh_snippets()
  ls.cleanup()
  M.reload_package("<update the module name here>")
end

local set = vim.keymap.set

local mode = { "i", "s" }
local normal = { "n" }

set(mode, "<c-i>", M.expand_or_jump)
set(mode, "<c-n>", M.jump_prev)
set(mode, "<c-l>", M.change_choice)
set(normal, ",r", M.refresh_snippets)
