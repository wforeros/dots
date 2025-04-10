return {
  {
    "rebelot/kanagawa.nvim",
    lazy = false,
    opts = {},
  },
  {
    "folke/tokyonight.nvim",
    lazy = false,
    opts = {},
  },
  {
    "marciomazza/vim-brogrammer-theme",
  },
  -- { "kartikp10/noctis.nvim", dependencies = { "rktjmp/lush.nvim" } },
  {
    "navarasu/onedark.nvim",
    config = function()
      require("onedark").setup({
        style = "cool",
      })
    end,
  },
  {
    "gmr458/vscode_modern_theme.nvim",
    lazy = false,
    config = function()
      require("vscode_modern").setup({
        cursorline = true,
        transparent_background = true,
        nvim_tree_darker = true,
      })
    end,
  },
  {
    "catppuccin/nvim",
    name = "catppuccin",
    lazy = false,
    opts = {
      transparent_background = true,
      flavour = "moccha",
      italic = false,
    },
  },
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
      -- colorscheme = "catppuccin-macchiato",
      colorscheme = "cyberdream",
      transparent_background = true,
    },
  },
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
    opts = {
      show_warnings = true,
    },
    config = function()
      require("modicator").setup({
        -- Warn if any required option is missing. May emit false positives if some
        -- other plugin modifies them, which in that case you can just ignore
        show_warnings = false,
        highlights = {
          -- Default options for bold/italic
          defaults = {
            bold = false,
            italic = false,
          },
        },
        integration = {
          lualine = {
            enabled = true,
            -- Letter of lualine section to use (if `nil`, gets detected automatically)
            mode_section = nil,
            -- Whether to use lualine's mode highlight's foreground or background
            highlight = "bg",
          },
        },
      })
    end,
  },
  --     {
  --       "lazyvim/lazyvim",
  jdw, --       opts = {
  --     --         colorscheme = "cyberdream",
  --     --       },
  --     --     },
  --     --   {
  --     {
  --       "scottmckendry/cyberdream.nvim",
  --       lazy = false,
  --       priority = 1000,
  --       opts = function(_, opts)
  --         opts.transparent = true
  --         opts.italic_comments = true
  --         opts.theme = {}
  --       end,
  --     },
  --     --
  --     -- -- modicator (auto color line number based on vim mode)
  --     -- {
  --     --   "mawkler/modicator.nvim",
  --     --   dependencies = "scottmckendry/cyberdream.nvim",
  --     --   init = function()
  --     --     -- These are required for Modicator to work
  --     --     vim.o.cursorline = false
  --     --     vim.o.number = true
  --     --     vim.o.termguicolors = true
  --     --   end,
  --     --   opts = {},
  --     -- },
  --   },
  -- },
}
