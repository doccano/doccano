#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
cd ..
unset DIR

# FOUND LINKS:
# app/server/templates/admin.html
# https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/vs2015.min.css

# app/server/templates/base.html
# https://use.fontawesome.com/releases/v5.0.13/css/all.css
# https://fonts.googleapis.com/css?family=Open+Sans:300,400,700
# https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css
# https://cdn.jsdelivr.net/npm/bulma-extensions@4.0.1/bulma-divider/dist/css/bulma-divider.min.css
# https://cdn.jsdelivr.net/npm/bulma-extensions@4.0.1/bulma-checkradio/dist/css/bulma-checkradio.min.css
# https://cdn.jsdelivr.net/npm/bulma-extensions@4.0.1/bulma-tooltip/dist/css/bulma-tooltip.min.css

# app/server/templates/index.html
# https://cdnjs.cloudflare.com/ajax/libs/Swiper/4.3.3/css/swiper.min.css

# https://source.unsplash.com/RWnpyGtY1aU
# https://source.unsplash.com/6Ticnhs1AG0
# https://i.imgsafe.org/ba/baa924a5e3.png

# frontend/nuxt.config.js
# https://use.fontawesome.com/releases/v5.0.6/js/all.js
# https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons

n_columns="2"
declare -a links=("offline/vs2015.min.css"           "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/vs2015.min.css"
                  "offline/all.css"                  "https://use.fontawesome.com/releases/v5.0.13/css/all.css"
                  "offline/opensans.css"             "https://fonts.googleapis.com/css?family=Open+Sans:300,400,700"
                  "offline/bulma.min.css"            "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css"
                  "offline/bulma-divider.min.css"    "https://cdn.jsdelivr.net/npm/bulma-extensions@4.0.1/bulma-divider/dist/css/bulma-divider.min.css"
                  "offline/bulma-checkradio.min.css" "https://cdn.jsdelivr.net/npm/bulma-extensions@4.0.1/bulma-checkradio/dist/css/bulma-checkradio.min.css"
                  "offline/bulma-tooltip.min.css"    "https://cdn.jsdelivr.net/npm/bulma-extensions@4.0.1/bulma-tooltip/dist/css/bulma-tooltip.min.css"
                  "offline/photo-1.jpg"              "https://source.unsplash.com/RWnpyGtY1aU"
                  "offline/photo-2.jpg"              "https://source.unsplash.com/6Ticnhs1AG0"
                  "offline/photo-3.jpg"              "https://i.imgsafe.org/ba/baa924a5e3.png"

                  "offline/all.js"                   "https://use.fontawesome.com/releases/v5.0.6/js/all.js"
                  "offline/google-roboto.css"        "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons"
                  )

static_dir_app="app/server/static/"
static_dir_frontend="frontend/static/"
mkdir -p "${static_dir_app}offline/"
mkdir -p "${static_dir_frontend}offline/"

# root replace directories
app_dir="app/server/templates"
frontend_dir="frontend"

for ((i = 0; i < $(expr "${#links[@]}" / "$n_columns"); ++i)); do
    idx_local=$(expr $i \* $n_columns + 0)
    idx_link=$(expr $i \* $n_columns + 1)
    local="${links[$idx_local]}"
    link="${links[$idx_link]}"

    echo "Storing file to $local: $link"
    wget --content-on-error -q --show-progress -O "${static_dir_app}${local}" $link 2>/dev/null
    if [ $? -eq 0 ]; then
        # Copy to frontend static dir
        cp "${static_dir_app}${local}" "${static_dir_frontend}${local}"
        # For Django: Use 'static' for template, use ^ as delimiter for sed
        find $app_dir      -type f -exec sed -i "s^${link}^{% static \'${local}\' %}^g" {} \;
        # For Vue: Use // for same host, use ^ as delimiter for sed
        find $frontend_dir -type f -exec sed -i "s^${link}^/${local}^g" {} \;
    else
        echo "Failed to transform for offline use: $link"
    fi
done
