



function docker_container_names() {
    docker ps -a --format "{{.Names}}" | xargs
}

# Get the IP address of a particular container
dip() {
    local network
    network='YOUR-NETWORK-HERE'
    docker inspect --format "{{ .NetworkSettings.Networks.$network.IPAddress }}" "$@"
}

dipall() {
    for container_name in $(docker_container_names);
    do
        local container_ip=$(dip $container_name)
        if [[ -n "$container_ip" ]]; then
            echo $(dip $container_name) " $container_name"
        fi
    done | sort -t . -k 3,3n -k 4,4n
}
