# NavUI
The navUI is just like any other navui. It is meant to be responsive
and compatible with all devices, and it is meant to support dropdown
menu's.

## Components
### Dropdown
This is an example of how you'd make a dropdown menu with the navUI
in the context of where you'd be making it.
```html
<!-- The full list of nav-btns and dropdowns. -->
<li>
    <!-- Other buttons and dropdowns. -->
    <div class="dropdown_btn_container">
        <a href="#" class="nav-btn">
            Btn Label
            <svg class="arrow"></svg>
        </a>
        <ul class="dropdown">
            <li><a href="#">Sub-Item 1</a></li>
            <li><a href="#">Sub-Item 2</a></li>
        </ul>
    </div>
    <!-- Other buttons and dropdowns. -->
</li>
```
### Nav Button
This is an example of how you'd make a nav button with the navUI
in the context of where you'd be making it.
```html
<!-- The full list of nav-btns and dropdowns. -->
<li>
    <!-- Other buttons and dropdowns. -->
    <a href="#" class="nav-btn">
        Btn Label
    </a>
    <!-- Other buttons and dropdowns. -->
</li>
```
### Nav button - Custom SVG
This is an example of how you'd make a nav button with a custom SVG
```html
<a href="#" class="nav-btn">
    <svg class="custom-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <!-- Your SVG code here. -->
    </svg>
    Btn Label
</a>
```