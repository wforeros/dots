return {
  "nvim-lualine/lualine.nvim",
  optional = true,
  opts = function(_, opts)
    if not vim.g.trouble_lualine then
      table.insert(opts.sections.lualine_c, {
        function()
          return require("nvim-navic").get_location()
        end,
        cond = function()
          return package.loaded["nvim-navic"] and require("nvim-navic").is_available()
        end,
      })
    end
  end,
}
