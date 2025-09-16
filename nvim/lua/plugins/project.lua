return {
  "ahmedkhalf/project.nvim",
  -- opts = {
  -- detection_methods = { "pattern", "lsp" },
  -- patterns = { ".git", "_darcs", ".hg", ".bzr", ".svn", "Makefile", "package.json", "apps/*" },
  -- },
  config = function(_, opts)
    require("project_nvim").setup(opts)
    local history = require("project_nvim.utils.history")
    history.delete_project = function(project)
      for k, v in pairs(history.recent_projects) do
        if v == project.value then
          history.recent_projects[k] = nil
          return
        end
      end
    end
    LazyVim.on_load("telescope.nvim", function()
      require("telescope").load_extension("projects")
    end)

    vim.keymap.set("n", "<leader>fp", function()
      require("telescope").extensions.projects.projects({})
    end, { desc = "Find projects" })
  end,
  -- config = function(_, opts)
  --   local project = require("project_nvim")
  --   project.setup(opts)
  --   pcall(require("telescope").load_extension, "projects")
  --   vim.keymap.set("n", "<leader>fp", function()
  --     require("telescope").extensions.projects.projects({})
  --   end, { desc = "Find projects" })
  -- end,
}
