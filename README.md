# 📸 Flask Webapp for a Photography Portfolio

This is a web-application built with Python, hosted for free on [PythonAnywhere](https://www.pythonanywhere.com), and used to display my personal photography portfolio.

The website is available to browse [here](http://ansla.pythonanywhere.com).
<br>
**💥Tip**: turn off 'Prevent cross-site tracking' or 'Prevent Cookies' in your browser to view images if they are not loading.
<br></br>
## Features

The webapp features a home page with album covers for each of my photo-series, each series (album) is accessible in its own subpage by clicking on the cover. To navigate back to the home page, each subpage contains a 'back' menu.

The site is run using **Flask** for its back-end, **Plotly** graphing library for displaying the map on the home page, and **HTML/CSS** for formatting the home page and photo-series subpages.

The code is hosted on GitHub and is continuously deployed at PythonAnywhere using their free resources, with updates to the website happening automatically after every `push` event.

All images are shot by me, edited using my own Adobe Lightroom presets (Lightroom is available for free on mobile), and are stored for free via my Google Drive.
<br>
**💥Tip**: loading large-resolution images from Google Drive might take a few seconds.

>### ✔️All the features can be recreated for free.
<br></br>
## Getting Started — Creating a Similar Webapp

### Working with Flask

[This brief tutorial](https://pythonhow.com/python-tutorial/flask) is helpful in understanding the basics of backend with Flask, the lessons also feature handy instructions for adding more pages to the webapp and creating a navigation menu. The [Quickstart Documentation](https://flask.palletsprojects.com/en/2.1.x/quickstart/) for Flask covers these fundamentals as well.

These two tutorials, [(1)](https://linuxhint.com/build-a-website-with-python/) and [(2)](https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask), go over the file structure, including the `static` directory for CSS and JS and the HTML `templates` files. The second link also explains the benefits of using the Flask micro-framework over Django, which is a good subject to explore more broadly.

### HTML and CSS

[W3Schools](https://www.w3schools.com/html/) and Stack Overflow are very useful in providing advice and snippets of CSS/HTML code for particular styling and visualisation needs, like adding links to images, styling headings, centering text, etc.

For image display in neat rows, I recommend exploring [Bootstrap 'grid' properties](https://getbootstrap.com/docs/4.0/layout/grid/), among other Bootstrap functionality.

### Image Storage and Access

Google Drive is a good storage option for free, although the final webapp load-time of the images can be slow. For convenient access to the links in a Google Sheets file, I sorted my series into folders and used the [Drive Explorer](https://workspace.google.com/marketplace/app/drive_explorer/520711270513) extension, but I advise you to read their 'Privacy Policy' before installing it onto your Drive.

### Geographical Data and Plotly

I add my locations to two lists (country + town) to then access their coordinates from [this dataset](https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/table/?disjunctive.cou_name_en&sort=name&location=12,51.477,-0.01854&basemap=jawg.light) available as a `csv`. I then use Pandas to match the locations with their lattitude and longitude values.
<br>
**💥Tip**: adding a country list is useful, because there may be multiple cities with the same name in the GeoNames dataset, and you can then end up with multiple 'Londons' in 3+ different countries.

I then work with the Plotly Python library to create a `scatter_mapbox` with custom settings to fit the display style of my site.
<br>
**💥Tip**: you will need to sign up to Mapbox and [generate your own access token](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/#how-access-tokens-work) to render Plotly charts.

Following [this helpful TDS tutorial](https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946), I finally 'dump' my Python Plotly chart into a JSON and use the following code to display the plot using Plotly.js:
```angular2html
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script type='text/javascript'>
    const graphs = {{graphJSON | safe}};
    graphs.config = {displayModeBar: false};
    Plotly.newPlot('chart', graphs);
</script>
```

**💥Tip**: the script needs to be outside the `<body>` tag, while the chart class item itself needs to be inside it: `<body><div id='chart' class='chart'></div></body>`.



### Hosting and Deployment

To create webapp hosting and ensure free continuous deployment at PythonAnywhere I recommend following the steps in [this video](https://www.youtube.com/watch?v=AZMQVI6Ss64). It explains how to use GitHub webhooks, git hooks, and the PythonAnywhere interface to host and seamlessly update your site.
<br>
**💥Tip**: in troubleshooting GitHub webhooks, check if your repository is public. Otherwise, the continuous deployment procedure described in the video may not work (`Error 500`). 
<br></br>
## License

The Ubuntu Mono font available through Google fonts is licenced with the copyleft [Ubuntu font license](https://ubuntu.com/legal/font-licence).

The countries-and-coordinates dataset stored in `geonames.csv` is compiled by GeoNames, accessible via Opendatasoft on [this site](https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/table/?disjunctive.cou_name_en&sort=name&location=12,51.477,-0.01854&basemap=jawg.light) with the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

The webapp's exact design and all images on the site are my property (©️), to be used with permission only.
<br></br>
## Contributors

Anastasia / [an-sla](https://github.com/an-sla)

[![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anastasia-slabucho-21b9b219b/)