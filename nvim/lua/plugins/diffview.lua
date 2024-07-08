return {
  "sindrets/diffview.nvim",
  lazy = false,
  priority = 1000,
  config = function()
    require("gitsigns").setup()
    vim.keymap.set("n", "<leader>gdo", ":DiffviewOpen <CR>", {})
    vim.keymap.set("n", "<leader>gdc", ":DiffviewClose <CR>", {})
  end,

  opts = {},
}
