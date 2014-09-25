#!/usr/bin/env python3
import os
import sys
class Server:
    def __init__(self, server_id, files_dir, md5_dir):
        self.server_id = server_id
        self.files_dir = files_dir
        self.md5_dir = md5_dir
    def run(self):
