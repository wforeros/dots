return {
  {
    "echasnovski/mini.nvim",
    version = "*",
    config = function()
      require("mini.files").setup({})
    end,
    keys = {
      {
        "<leader>fm",
        function()
          require("mini.files").open()
        end,
        desc = "Open mini file manager",
      },
    },
  },
}
