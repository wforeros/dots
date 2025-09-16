hs.hotkey.bind({ "alt" }, ",", function()
	local runningApps = hs.application.runningApplications()
	local choices = {}

	for _, app in ipairs(runningApps) do
		local appName = app:name()
		local path = app:path()

		local isDockApp = appName
			and not app:isHidden()
			and app:kind() == 1
			and path
			and (path:match("^/Applications/") or path:match("^/System/Applications/"))

		if isDockApp then
			table.insert(choices, {
				text = appName,
				subText = path,
				app = app,
			})
		end
	end

	local chooser = hs.chooser.new(function(choice)
		if choice and choice.app then
			choice.app:activate()
		end
	end)

	chooser:choices(choices)
	chooser:placeholderText("Escribe para buscar en las apps abiertas")
	chooser:searchSubText(true)
	chooser:show()
end)
