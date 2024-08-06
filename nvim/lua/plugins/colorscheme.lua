return {
  {
    "rebelot/kanagawa.nvim",
    lazy = false,
    priority = 1000,
    opts = {},
  },
  -- {
  --   "gmr458/vscode_modern_theme.nvim",
  --   lazy = false,
  --   priority = 1000,
  --   config = function()
  --     require("vscode_modern").setup({
  --       cursorline = true,
  --       transparent_background = true,
  --       nvim_tree_darker = true,
  --     })
  --     vim.cmd.colorscheme("vscode_modern")
  --   end,
  -- },
  { "catppuccin/nvim", name = "catppuccin", priority = 1001, lazy = false, opts = { flavour = "macchiato" } },
  {
    "xiyaowong/transparent.nvim",
    config = function()
      require("transparent").setup({ -- Optional, you don't have to run setup.
        groups = { -- table: default groups
          "Normal",
          "NormalNC",
          "Comment",
          "Constant",
          "Special",
          "Identifier",
          "Statement",
          "PreProc",
          "Type",
          "Underlined",
          "Todo",
          "String",
          "Function",
          "Conditional",
          "Repeat",
          "Operator",
          "Structure",
          "LineNr",
          "NonText",
          "SignColumn",
          "CursorLine",
          "CursorLineNr",
          "StatusLine",
          "StatusLineNC",
          "EndOfBuffer",
        },
        extra_groups = {
          "NormalFloat", -- plugins which have float panel such as Lazy, Mason, LspInfo
          "NvimTreeNormal", -- NvimTree
          "NvimTreeNormalNC", -- NvimTree
        },
        exclude_groups = {}, -- table: groups you don't want to clear
      })
    end,
    {
      {
        "scottmckendry/cyberdream.nvim",
        lazy = false,
        priority = 1000,
        opts = function(_, opts)
          opts.transparent = true
          opts.italic_comments = true
        end,
      },
      {
        "LazyVim/LazyVim",
        opts = {
          colorscheme = "cyberdream",
        },
      },

      -- modicator (auto color line number based on vim mode)
      {
        "mawkler/modicator.nvim",
        dependencies = "scottmckendry/cyberdream.nvim",
        init = function()
          -- These are required for Modicator to work
          vim.o.cursorline = false
          vim.o.number = true
          vim.o.termguicolors = true
        end,
        opts = {},
      },
    },
  },
}
