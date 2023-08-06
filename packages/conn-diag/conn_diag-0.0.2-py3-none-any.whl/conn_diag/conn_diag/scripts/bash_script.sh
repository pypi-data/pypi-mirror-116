#!/usr/bin/env bash

TIMEOUT=''
SOCKETS=''
DELIMITER=''
LINE_SEPARATOR=''


function telnet {
  for socket in $(echo "$SOCKETS" | tr "$LINE_SEPARATOR" "\n"); do
    ip=$(echo "$socket" | cut -f1 -d "$DELIMITER")
    port=$(echo "$socket" | cut -f2 -d "$DELIMITER")
    result=$(echo 'quite' | timeout "$TIMEOUT" telnet "$ip" "$port" 2>&1)
    exit_status="$?"

    details=$(echo "$result" | tr "\n" "\s")

    if [ $exit_status == 124 ]; then
      echo "timeout${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
      continue
    fi

    if [[ $result =~ 'Connected' ]]; then
      echo "connected${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    elif [[ $result =~ 'refused' ]]; then
      echo "refused${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    else
      echo "timeout${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    fi
  done
}

function nc {
  for socket in $(echo "$SOCKETS" | tr "$LINE_SEPARATOR" "\n"); do
    ip=$(echo "$socket" | cut -f1 -d "$DELIMITER")
    port=$(echo "$socket" | cut -f2 -d "$DELIMITER")
    result=$(nc -v -w "$TIMEOUT" "$ip" "$port" 2>&1)
    details=$(echo "$result" | tr "\n" "\s")

    if [[ $result =~ 'timed out' ]]; then
      echo "timeout${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    elif [[ $result =~ 'succeeded' || $result =~ 'Connected' ]]; then
      echo "connected${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    elif [[ $result =~ 'refused' ]]; then
      echo "refused${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    else
      echo "timeout${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    fi
  done
}

function bash {
  for socket in $(echo "$SOCKETS" | tr "$LINE_SEPARATOR" "\n"); do
    ip=$(echo "$socket" | cut -f1 -d "$DELIMITER")
    port=$(echo "$socket" | cut -f2 -d "$DELIMITER")
    result=$(timeout "$TIMEOUT" bash -c "</dev/tcp/$ip/$port" 2>&1)
    exit_status="$?"
    details=$(echo "$result" | tr "\n" "\s")

    if [ $exit_status == 0 ]; then
      echo "connected${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    elif [ $exit_status == 124 ]; then
      echo "timeout${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    elif [[ $result =~ 'refused' ]]; then
      echo "refused${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    else
      echo "timeout${DELIMITER}${ip}${DELIMITER}${port}${DELIMITER}${details}"
    fi
  done
}

if which telnet > /dev/null 2>&1; then
  telnet
elif which nc > /dev/null 2>&1; then
  nc
else
  bash
fi