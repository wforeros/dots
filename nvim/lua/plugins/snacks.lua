-- Inspired by: https://github.com/linkarzu/dotfiles-latest/blob/main/neovim/neobean/lua/plugins/snacks.lua
return {
  "snacks.nvim",
  keys = {
    {
      "<M-b>",
      function()
        Snacks.picker.git_branches({
          layout = "select",
        })
      end,
      desc = "Branches",
    },
  },
  opts = {
    lazygit = {
      theme = {
        selectedLineBgColor = { bg = "CursorLine" },
      },
      -- With this I make lazygit to use the entire screen, because by default there's
      -- "padding" added around the sides
      -- I asked in LazyGit, folke didn't like it xD xD xD
      -- https://github.com/folke/snacks.nvim/issues/719
      win = {
        -- -- The first option was to use the "dashboard" style, which uses a
        -- -- 0 height and width, see the styles documentation
        -- -- https://github.com/folke/snacks.nvim/blob/main/docs/styles.md
        -- style = "dashboard",
        -- But I can also explicitly set them, which also works, what the best
        -- way is? Who knows, but it works
        width = 0,
        height = 0,
      },
    },
    picker = {
      -- My ~/github/dotfiles-latest/neovim/lazyvim/lua/config/keymaps.lua
      -- file was always showing at the top, I needed a way to decrease its
      -- score, in frecency you could use :FrecencyDelete to delete a file
      -- from the database, here you can decrease it's score
      transform = function(item)
        if not item.file then
          return item
        end
        -- Demote the "lazyvim" keymaps file:
        if item.file:match("lazyvim/lua/config/keymaps%.lua") then
          item.score_add = (item.score_add or 0) - 30
        end
        return item
      end,
      -- In case you want to make sure that the score manipulation above works
      -- or if you want to check the score of each file
      debug = {
        scores = false, -- show scores in the list
      },
      -- I like the "ivy" layout, so I set it as the default globaly, you can
      -- still override it in different keymaps
      layout = {

        -- "ivy",
        -- "ivy_wider_results",
        -- "ivy_wider_preview",
        -- "ivy_taller",
        preset = "ivy",
        -- When reaching the bottom of the results in the picker, I don't want
        -- it to cycle and go back to the top
        cycle = false,
      },
      layouts = {
        -- I wanted to modify the ivy layout height and preview pane width,
        -- this is the only way I was able to do it
        -- NOTE: I don't think this is the right way as I'm declaring all the
        -- other values below, if you know a better way, let me know
        --
        -- Then call this layout in the keymaps above
        -- got example from here
        -- https://github.com/folke/snacks.nvim/discussions/468
        ivy = {
          layout = {
            box = "vscode",
            backdrop = false,
            row = -1,
            width = 0,
            height = 0.5,
            border = "top",
            title = " {title} {live} {flags}",
            title_pos = "left",
            { win = "input", height = 1, border = "bottom" },
            {
              box = "horizontal",
              { win = "list", border = "none" },
              { win = "preview", title = "{preview}", width = 0.5, border = "left" },
            },
          },
        },
        -- I wanted to modify the layout width
        --
        vertical = {
          layout = {
            backdrop = false,
            width = 0.8,
            min_width = 80,
            height = 0.8,
            min_height = 30,
            box = "vertical",
            border = "rounded",
            title = "{title} {live} {flags}",
            title_pos = "center",
            { win = "input", height = 1, border = "bottom" },
            { win = "list", border = "none" },
            { win = "preview", title = "{preview}", height = 0.4, border = "top" },
          },
        },
      },
      matcher = {
        frecency = true,
      },
      win = {
        input = {
          keys = {
            -- to close the picker on ESC instead of going to normal mode,
            -- add the following keymap to your config
            ["<Esc>"] = { "close", mode = { "n", "i" } },
            -- I'm used to scrolling like this in LazyGit
            ["J"] = { "preview_scroll_down", mode = { "i", "n" } },
            ["K"] = { "preview_scroll_up", mode = { "i", "n" } },
            ["H"] = { "preview_scroll_left", mode = { "i", "n" } },
            ["L"] = { "preview_scroll_right", mode = { "i", "n" } },
          },
        },
      },
      formatters = {
        file = {
          filename_first = true, -- display filename before the file path
          truncate = 80,
        },
      },
    },
    dashboard = {
      preset = {
        header = [[
██╗    ██╗    ███████╗ ██████╗ ██████╗     ██████╗ ███████╗██╗   ██╗███████╗
██║    ██║    ██╔════╝██╔═══██╗██╔══██╗    ██╔══██╗██╔════╝██║   ██║██╔════╝
██║ █╗ ██║    █████╗  ██║   ██║██████╔╝    ██║  ██║█████╗  ██║   ██║███████╗
██║███╗██║    ██╔══╝  ██║   ██║██╔══██╗    ██║  ██║██╔══╝  ╚██╗ ██╔╝╚════██║
╚███╔███╔╝    ██║     ╚██████╔╝██║  ██║    ██████╔╝███████╗ ╚████╔╝ ███████║
 ╚══╝╚══╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚══════╝  ╚═══╝  ╚══════╝
                 
     ▀▄     ▄▀     
    ▄██▀███▀██▄    
   █▀█████████▀█   
   █ ██▀▀▀▀▀██ █   
      ▀▀▀ ▀▀▀      
        ]],
        -- stylua: ignore
        ---@type snacks.dashboard.Item[]
        keys = {
          { icon = " ", key = "f", desc = "Find File", action = ":lua Snacks.dashboard.pick('files')" },
          { icon = " ", key = "n", desc = "New File", action = ":ene | startinsert" },
          { icon = " ", key = "g", desc = "Find Text", action = ":lua Snacks.dashboard.pick('live_grep')" },
          { icon = " ", key = "r", desc = "Recent Files", action = ":lua Snacks.dashboard.pick('oldfiles')" },
          { icon = " ", key = "c", desc = "Config", action = ":lua Snacks.dashboard.pick('files', {cwd = vim.fn.stdpath('config')})" },
          { icon = " ", key = "s", desc = "Restore Session", section = "session" },
          { icon = " ", key = "x", desc = "Lazy Extras", action = ":LazyExtras" },
          { icon = "󰒲 ", key = "l", desc = "Lazy", action = ":Lazy" },
          { icon = " ", key = "q", desc = "Quit", action = ":qa" },
        },
      },
    },
  },
}
