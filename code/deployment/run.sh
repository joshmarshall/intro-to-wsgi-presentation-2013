#!/bin/sh

gunicorn -w 4 app:app