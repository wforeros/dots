return {
  {
    "folke/zen-mode.nvim",
    enabled = false,
    keys = {
      {
        "<leader>z",
        function()
          require("zen-mode").toggle()
        end,
        desc = "Zen Mode",
      },
    },
    opts = {
      window = {
        width = 0.85,
      },
      plugins = {
        options = {
          laststatus = 0,
        },
        twilight = {
          enabled = false,
        },
      },
      on_open = function()
        require("package-info").hide()
      end,
    },
  },
}
