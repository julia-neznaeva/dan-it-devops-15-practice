#!/bin/bash

HIDDEN_NUMERIC=$((RANDOM % 100 + 1))
GUESS=0
ATTEMPT=0

while [ $ATTEMPT -lt 5 ]
do
    read -p "Enter your guess: " GUESS

    if [ $HIDDEN_NUMERIC -eq $GUESS ]; then
        echo "Congratulations! You guessed the right number."
        exit 0

    elif [ $HIDDEN_NUMERIC -lt $GUESS ]; then
        echo "Too high"

    elif [ $HIDDEN_NUMERIC -gt $GUESS ]; then
        echo "Too low"
    fi

    ATTEMPT=$((ATTEMPT + 1))
done

echo "Sorry, you are out of attempts."
echo "The correct number was $HIDDEN_NUMERIC"

