import os
import argparse

def setup_studio_env(studio_name, nuke_version, maya_version, artist_name):
    os.environ["STUDIO_NAME"] = studio_name
    os.environ["NUKE_VERSION"] = nuke_version
    os.environ["MAYA_VERSION"] = maya_version
    os.environ["ARTIST_NAME"] = artist_name
    
    print("Studio Environment Variables Set:")
    print(f"STUDIO_NAME: {os.environ['STUDIO_NAME']}")
    print(f"NUKE_VERSION: {os.environ['NUKE_VERSION']}")
    print(f"MAYA_VERSION: {os.environ['MAYA_VERSION']}")
    print(f"ARTIST_NAME: {os.environ['ARTIST_NAME']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up the studio environment variables.")
    
    parser.add_argument("-s", "--studio", type=str, default="Pixomondo", help="Set the studio name (default: Pixomondo)")
    parser.add_argument("-n", "--nuke", type=str, default="14.0v5", help="Set the Nuke version (default: 14.0v5)")
    parser.add_argument("-m", "--maya", type=str, default="2023", help="Set the Maya version (default: 2023)")
    parser.add_argument("-a", "--artist", type=str, default="John Doe", help="Set the artist name (default: John Doe)")

    args = parser.parse_args()

    setup_studio_env(args.studio, args.nuke, args.maya, args.artist)

# python3 argparse_Exercise.py --studio Framestore --nuke 13.2v4 --maya 2022 --artist 'Kunal Dekhane'
