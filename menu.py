# menu.py
class MenuItem(object):
	def __init__(self, type, name, attributes = None, visible = True):
		self.type = type
		self.name = name
		self.attributes = attributes
		self.visible = visible

class Back(MenuItem):
	def __init__(self, name):
		MenuItem.__init__(self, "back", name)

class Menu(MenuItem):
	def __init__(self, name, attributes = None, visible = True):
		MenuItem.__init__(self, "menu", name, attributes, visible)
		self.options = []
		self.selectedOption = 0
		self.parent = None

	def addOptions(self, options):
		self.options = self.options + options
		self.selectedOption = 0

	def addOption(self, option):
		self.options.append(option)
		self.selectedOption = 0

	def setParent(self, parent):
		self.parent = parent

	def nextSelection(self):
		self.selectedOption = (self.selectedOption + 1) % len(self.options)

	def getSelection(self):
		return self.options[self.selectedOption]

class MenuContext(object):
	def __init__(self, menu, delegate):
		self.topLevelMenu = menu
		self.currentMenu = menu
		self.delegate = delegate
		self.showMenu()

	def showMenu(self):
		"""
		Shows the first selection of the current menu 
		"""
		self.display(self.currentMenu.getSelection());

	def setMenu(self, menu):
		"""
		Sets a new menu to the menu context.

		raises ValueError if the menu has no options
		"""
		if (len(menu.options) == 0):
			raise ValueError("Cannot setMenu on a menu with no options")
		self.topLevelMenu = menu
		self.currentMenu = menu
		self.showMenu();

	def display(self, menuItem):
		"""
		Tells the delegate to display the selection. Advances to the next selection if the 
		menuItem is visible==False
		"""
		self.delegate.prepareForRender(self.topLevelMenu)
		if (not menuItem.visible):
			self.advance()
		else:
			self.delegate.displayMenuItem(menuItem)

	def advance(self):
		"""
		Advances the displayed menu to the next visible option

		raises ValueError if all options are visible==False
		"""
		for i in self.currentMenu.options:
			self.currentMenu.nextSelection()
			selection = self.currentMenu.getSelection()
			if (selection.visible): 
				self.display(selection)
				return
		raise ValueError("At least one option in a menu must be visible!")

	def select(self):
		"""
		Selects the current menu option. Calls menuItemClicked first. If it returns false,
		it uses the default logic. If true, it calls display with the current selection

		defaults:
			"menu" -> sets submenu as the current menu
			"back" -> sets parent menu as the current menu

		returns True if the default logic should be overridden

		throws ValueError if navigating back on a top-level menu

		"""
		selection = self.currentMenu.getSelection()
		if (not self.delegate.menuItemClicked(selection)):
			if (selection.type is "menu"):
				self.setMenu(selection)
			elif (selection.type is "back"):
				if (not self.currentMenu.parent):
					raise ValueError("Cannot navigate back when parent is None")
				self.setMenu(self.currentMenu.parent)
		else:
			self.display(self.currentMenu.getSelection())

class MenuDelegate(object):
	def prepareForRender(self, menu): 
		"""
		Called before the menu needs to display. Useful for changing visibility. 
		"""
		raise NotImplementedError

	def menuItemClicked(self, menuItem):
		"""
		Called when a menu item is selected. Useful for taking action on a menu item click.
		"""
		raise NotImplementedError

	def displayMenuItem(self, menuItem):
		"""
		Called when the menu item should be displayed.
		"""
		raise NotImplementedError
