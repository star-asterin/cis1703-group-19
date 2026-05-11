# cis1703-group-19
Group 19's scenario is SmartStock

## Group members (alphabetical order):
-	Bruno Banas 26610361 – Developer – brunobanas1982-sketch
-	Thomas Copeland 26126567 – Project Manager – Thomalexc
-	Konstantin Karaychev 26555891 – Lead Architect – rollrkostr
-	Haillie Tiger Lyons 26617137 – QA Lead – haisakataiga
-	Angel Prus 26454289 – UI/UX Designer (Team Leader) – star-asterin
-	Isaac Quartermaine 26548470 – QA Lead – IsaacIPLoF

> [!NOTE]
> Dependencies: Python - \
> Imported libraries are automatically managed by Python, so this is the only requirement for this program.

# Instructions:

## Products:
- Displayed in a listbox in the centre of the window.
- Newly created items display information in the following order:
- `Product Type: ID, Name, Price (£), Quantity`.
- Perishable items have `Expiry Date` and `Storage Temperature (°C OR °F)`.
- Electronic items have `Warranty Period (months)` and `Power Usage (W)`.

## Main window:
- 7 buttons, clearly labelled. Clicking the buttons either directly performs the associated action or opens a new window for further input.
- Status messages at the top of the window give the user confirmation for actions, and informs them of what to do when something goes wrong.
- The Listbox in the centre of the screen shows all items currently loaded. Items with 5 or less stock are marked with a red background.
- Helpful text at the bottom of the window, allowing for more save/load options.

## Add Stock window:
- Clear headings show users what goes where.
- Dropdown menu changes type of product created.
> [!NOTE]
> Changing the product type changes the relevant input fields, e.g. electronic products have power usage (in Watts), etc.
- Item ID is created automatically upon item creation.
- Input validated fields, e.g. item name accepts string, item price = float, item quantity = int, etc.
- Unique status below the final entry field tells users if an error occurs, and what the user should do.

## Edit Stock window:
- Tells the user which item they are editing, by showing item ID.
- All fields are filled in pre-emptively so the user does not have to fill every field out when changing one attribute.
- Simple "Save Changes" button updates the item in the listbox. Once clicked, the window closes automatically.

## Transaction history window:
- Shows the user a list of previous actions taken, giving an exact time and action taken.
- Example: `[2026-05-11 21:12:34] Loaded default inventory [inventorySave.json]`.

## Health Report:
- Displays information about all stock in the current inventory, in the following order:
- Total Items
- Percentage of each product type in the inventory (e.g. `50% Regular | 37.5% Perishable | 12.5% Electronic`)
- Low stock alerts
- Expiring stock (and how long until expiry)
- Expired stock (and how long since expiry)
- Total value of items
- Value breakdown (percentage of each product price*quantity compared to total value)

## Total Cost button:
- Quick way of displaying the total value of items in the current inventory.
> [!NOTE]
> Only updates when the button is pressed.

## Alternative Save/Load features:
- Holding 'Shift' key will show alternative save/load options, as stated on the main window.
- Clicking `Save inventory as. . .` will display a save popup, where the user can choose a title for the inventory and where it is saved.
- Clicking `Load inventory from. . .` will bring up a similar popup, where the user chooses a JSON file aside from the default inventory.
- Clicking `Save inventory` after loading a different inventory will automatically save the inventory in the chosen file destination.
> [!WARNING]
> Loading an inventory will not display the low stock items on the main window.
