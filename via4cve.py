if __name__ == '__main__':
  import argparse
  import json
  
  from lib.PluginManager import PluginManager
  
  description='''Generator script for VIA4'''
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('file', metavar='file', nargs='?',   help='Output location ( Default: VIA4CVE-feed.json)')
  parser.add_argument('--no-update',  action='store_true', help="DEBUG: don't run the update part of the sources")
  parser.add_argument('--no-cleanup', action='store_true', help="DEBUG: don't run the cleanup part of the sources")

  args = parser.parse_args()

  pm = PluginManager()                                         # Create plug-in manager
  pm.loadPlugins()                                             # Load all sources & parse data

  cves = {}                                                    # Create empty dictionary to fill up
  path = args.file if args.file else "VIA4CVE-feed.json"       # Generate path based on user preferences

  for _id in pm.getAllCVEIDs(): cves[_id] = pm.getCVERefs(_id) # Get data per CVE
  if not args.no_update:
    for _id in cves.keys():     pm.updateRefs(_id, cves[_id])  # Update data based on previous data
  if not args.no_cleanup:
    for _id in cves.keys():     pm.cleanUp(_id, cves[_id])     # Clean data
  
  open(path, "w").write(json.dumps(cves))                      # Write data to path
