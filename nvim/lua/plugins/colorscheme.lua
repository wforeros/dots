return {
  {
    "rebelot/kanagawa.nvim",
    lazy = false,
    priority = 1000,
    opts = {},
  },
  {
    "gmr458/vscode_modern_theme.nvim",
    lazy = false,
    priority = 1000,
    config = function()
      require("vscode_modern").setup({
        cursorline = true,
        transparent_background = false,
        nvim_tree_darker = true,
      })
      vim.cmd.colorscheme("vscode_modern")
    end,
  },
  -- {
  --   "olimorris/onedarkpro.nvim",
  --   priority = 1000, -- Ensure it loads first
  -- },
  -- config = function()
  --   require("onedarkpro").setup({
  --     colors = {}, -- Override default colors or create your own
  --     highlights = {}, -- Override default highlight groups or create your own
  --     styles = { -- For example, to apply bold and italic, use "bold,italic"
  --       types = "BOLD", -- Style that is applied to types
  --       methods = "BOLD", -- Style that is applied to methods
  --       numbers = "NONE", -- Style that is applied to numbers
  --       strings = "NONE", -- Style that is applied to strings
  --       comments = "NONE", -- Style that is applied to comments
  --       keywords = "NONE", -- Style that is applied to keywords
  --       constants = "NONE", -- Style that is applied to constants
  --       functions = "BOLD", -- Style that is applied to functions
  --       operators = "NONE", -- Style that is applied to operators
  --       variables = "NONE", -- Style that is applied to variables
  --       parameters = "NONE", -- Style that is applied to parameters
  --       conditionals = "NONE", -- Style that is applied to conditionals
  --       virtual_text = "NONE", -- Style that is applied to virtual text
  --     },
  --   })
  -- end,
}
-- { "catppuccin/nvim", name = "catppuccin", lazy = false, opts = { flavour = "macchiato" } },
-- {
--   "LazyVim/LazyVim",
--   opts = {
--     colorscheme = "catppuccin",
--   },
-- },
