return {
  "danymat/neogen",
  config = function()
    -- code
    require("neogen").setup({
      enabled = true,
      languages = {
        lua = {
          template = {
            annotation_convention = "emmylua",
            -- for a full list of annotation_conventions, see supported-languages below,
            -- for more template configurations, see the language's configuration file in configurations/{lang}.lua
          },
        },
        sh = {
          template = {
            annotation_convention = "google",
          },
        },
        python = {
          template = {
            annotation_convention = "numpydoc",
          },
        },
        ruby = {
          template = {
            annotation_convention = "yard",
          },
        },
        javascript = {
          template = {
            annotation_convention = "jsdoc",
          },
        },
        javascriptreact = {
          template = {
            annotation_convention = "jsdoc",
          },
        },
        typescript = {
          template = {
            annotation_convention = "tsdoc",
          },
        },
        typescriptreact = {
          template = {
            annotation_convention = "tsdoc",
          },
        },
      },
    })
  end,
  version = "*",
  keys = {
    { "<leader>cg", "<cmd>lua require('neogen').generate()<cr>", desc = "Generate doc string" },
  },
}
