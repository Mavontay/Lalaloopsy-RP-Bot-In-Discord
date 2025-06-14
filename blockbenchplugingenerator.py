#!/usr/bin/env python3
import os
import argparse
import json
import textwrap

LALALOOPSY_CHARACTERS = [
    "Crumbs Sugar Cookie",
    "Spot Splatter Splash",
    "Rosy Bumps 'N' Bruises",
    "Mittens Fluff 'N' Stuff"
]

def generate_plugin_js(name, plugin_id, author, description, version):
    characters_js = json.dumps(LALALOOPSY_CHARACTERS, indent=4)
    return textwrap.dedent(f"""
        (function() {{
            const plugin = {{
                id: '{plugin_id}',
                title: '{name}',
                icon: 'fa-doll',
                author: '{author}',
                description: '{description}',
                version: '{version}',
                variant: 'both'
            }};

            const CHARACTERS = {characters_js};

            Plugin.register(plugin, function(api) {{
                let action = new Action('show_lalaloopsy_characters', {{
                    name: 'Show Lalaloopsy Characters',
                    description: 'Open a dialog listing Lalaloopsy characters.',
                    icon: 'fa-list',
                    click() {{
                        Blockbench.showQuickMessage(CHARACTERS.join("\\n"));
                    }}
                }});
                MenuBar.addAction(action, 'help');
            }});
        }})();
    """).strip()

def create_plugin(args):
    plugin_id = args.id.lower().replace(' ', '_')
    plugin_dir = os.path.join(os.getcwd(), plugin_id)
    os.makedirs(plugin_dir, exist_ok=True)

    plugin_js = generate_plugin_js(args.name, plugin_id, args.author, args.description, args.version)
    js_path = os.path.join(plugin_dir, f"{plugin_id}.js")
    with open(js_path, "w") as f:
        f.write(plugin_js)

    characters_path = os.path.join(plugin_dir, "lalaloopsy_characters.json")
    with open(characters_path, "w") as f:
        json.dump(LALALOOPSY_CHARACTERS, f, indent=4)

    print(f"Plugin generated at {plugin_dir}")

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a Blockbench plugin skeleton.")
    parser.add_argument('--name', required=True, help='Plugin display name')
    parser.add_argument('--id', required=True, help='Plugin identifier')
    parser.add_argument('--author', default='Unknown', help='Plugin author')
    parser.add_argument('--description', default='A Blockbench plugin', help='Plugin description')
    parser.add_argument('--version', default='1.0.0', help='Plugin version')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    create_plugin(args)
