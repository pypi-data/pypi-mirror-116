# :pencil2: Journalx: Supercharge your Obsidian Vault

Journalx makes it easy to use your Obsidian vault as the content
source for your [hugo](https://gohugo.io) website.

It's still in early stages and requires a lot of work, but it's useful right away if you have some key ingredients in place.

### Prerequisites

- Python environment with Journalx installed
- Hugo blog setup

Your obsidian vault contains a lot of documents, but you want to publish only some them. Journalx handles:

- Automatically transfering documents that are tagged for publishing
- Transfers images to destination directory, and substitutes image paths in markdown
- [WIP] Watch dir for changes, and transfer on change
- [WIP] Build and publish after transfering documents
- [WIP] Handle other static assets other than files
- [WIP] Allow doc metadata to be specified by config file
- [WIP] Unit test for different scenarios
- [WIP] Better help messages


## Install

You can install `journalx` using pip


## Commands

### Publishing

`config.ini` file contains settings which dictate the base directory of your [hugo](https://gohugo.io) website.
To create the config if it's not present

```bash
jx init --publish-dir <publish-dir>
```

Add metadata to `md` documents in your vault. This is required for publishing which looks for metadata values `publish: True` and `draft: False` in the document's metadata header.
If your documents don't have a yaml header (or only some of them do, not all), you can add it to all documents by
```bash
jx add-metadata
```

After you're done adding metadata, you can turn `publish:True` and `draft:False` on documents you want to publish.
The publish command make sure that they'll be transfered to configured `{publish_dir}/content/post` directory while the images 
that are present in the document will be transfered to `{publish_dir}/static/images` and the image links will be updated.

```bash
jx publish
```

 