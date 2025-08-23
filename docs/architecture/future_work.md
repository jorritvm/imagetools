# Future work architecture notes

<!-- TOC -->

* [Future work architecture notes](#future-work-architecture-notes)
    * [Adding a catalog module to the project to persist metadata](#adding-a-catalog-module-to-the-project-to-persist-metadata)
        * [Q: Store metadata centrally or distributed per picture folder?](#q-store-metadata-centrally-or-distributed-per-picture-folder)
        * [Q: Store metadata in text or binary format?](#q-store-metadata-in-text-or-binary-format)
        * [Q: How to avoid rewriting the entire metadata store for every change?](#q-how-to-avoid-rewriting-the-entire-metadata-store-for-every-change)
    * [FolderSelect - Catalog - Browser interaction](#folderselect---catalog---browser-interaction)
    * [Catalog - Operations interaction:](#catalog---operations-interaction)

<!-- TOC -->

## Adding a catalog module to the project to persist metadata

Over time it became apparent that persisted metadata handling was required.

- To select pictures that were previously not imported a tracking mechanism of pictures was needed.
- To avoid regenerating thumbnails for pictures that were already processed, a cache was needed.

#### Q: Store metadata centrally or distributed per picture folder?

- The metadata will be stored in the separate picture folders.
- This allows for easy backup meaning it will be available on other devices using imagetools too.

#### Q: Store metadata in text or binary format?

- The textual metadata will become part of a single JSON file (metadata.json) stored in every folder.
- The thumbnails will be stored as jpg in a subfolder (.thumbs)

#### Q: How to avoid rewriting the entire metadata store for every change?

- The textual metadata will be updated in bulk or when the folder changes and some entry is 'dirty'
- The thumbnails will be updated as they are generated. They are cleaned up when the folder is changed.

## FolderSelect - Catalog - Browser interaction

Interaction workflow:

- User interaction changes folder
- FolderSelect triggers folder_change in catalog
- Catalog cleans up old folder metadata
- Catalog loads new folder metadata from disk
- Catalog triggers folder_change in browser
- Browser loads new folder metadata from catalog (thumb or details view)
- If browser requested thumbnail view catalog will start generating missing thumbnails
- If a thumbnail is generated it will be stored in the catalog and sent to the browser

## Catalog - Operations interaction:

The catalog will only be used when using the UI interface. Not when using the CLI.
(This means modules like auto-select, which rely on persisted metadata, cannot be implemented in the CLI interface.) 