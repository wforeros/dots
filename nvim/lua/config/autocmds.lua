-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
-- Add any additional autocmds here

vim.api.nvim_create_autocmd("BufNewFile", {
  pattern = "*.html",
  callback = function()
    vim.opt.filetype = "htmldjango"
  end,
})

vim.api.nvim_create_autocmd("BufRead", {
  pattern = "*.html",
  callback = function()
    vim.opt.filetype = "htmldjango"
  end,
})
