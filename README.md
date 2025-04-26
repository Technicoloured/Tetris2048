# Tetris 2048

A Python implementation of a hybrid game combining the mechanics of **Tetris** and **2048**, developed as a project for the COMP 204 Programming Studio course.

## Team Members

- Sudenur Bilgin  
- Pınar Günal  
- Melike Gürcan  

## Overview

Tetris 2048 is a grid-based game where each tetromino is composed of four numbered tiles (initially 2 or 4). The objective is to:
- Clear full horizontal lines (Tetris-style)
- Merge vertically stacked tiles with equal numbers (2048-style)
- Reach a tile with a value of **2048** to win the game

The game ends either when the player achieves a 2048 tile or when new tetrominoes can no longer enter the grid due to lack of space.

## Features

- Full implementation of all 7 standard tetromino shapes (`I`, `O`, `T`, `S`, `Z`, `L`, `J`)
- Vertical merging with support for chain merges
- Row clearing with score calculation based on tile values
- Removal and scoring of disconnected/free tiles
- Real-time scoreboard display
- Next piece preview
- Pause and restart functionality
- Game over and win condition handling
- Start menu with image and start button
- Basic sound and row-clear animation

## Controls

- `←` / `→`: Move left / right  
- `↓`: Soft drop  
- `↑`: Rotate  
- `Space`: Hard drop  
- `P`: Pause / Resume  
- `R`: Restart  

## How to Run

Make sure Python 3 is installed on your system. Then run the game using:

```bash
python Tetris_2048.py
