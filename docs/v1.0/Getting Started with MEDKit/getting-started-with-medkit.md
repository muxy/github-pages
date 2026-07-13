---
title: "Get Started with MEDKit"
slug: "getting-started-with-medkit"
excerpt: "Introduction to MEDKit and the Muxy SDK"
hidden: false
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Sep 14 2021 23:26:02 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Dec 08 2021 21:10:52 GMT+0000 (Coordinated Universal Time)"
---
MEDKit is a JavaScript library for building viewer-facing extensions on Twitch. It is part of an SDK designed to make building and interacting with a Twitch extension easy. The complete SDK also includes APIs that let a Twitch developer interact directly with the Muxy server to integrate their game or other broadcast content with viewer data. You can communicate directly over HTTP using the [REST API](docs:developing-with-medkit), which MEDKit methods use, or using the GameLink Libraries, available for [C# and Unity](docs:integrate-with-unity) or [C++ and Unreal](docs:install-the-muxy-plugin-for-unreal-engine).

> 👍 Game Developers
> 
> If you use the Unreal Engine or Unity game-development environment, add a Muxy-powered experience using integrated Muxy functionality.   
> 
>  See [Integrate with Game-development Environments](#integrate-with-game-development-environments)

# Getting oriented

If you are writing extensions from the ground up, the first thing for you to do is get familiar with Muxy architecture and conventions. 

MEDKit comes with an [extension starter project](https://github.com/muxy/medkit-starter-vue) that includes the installed and configured library. The easiest and fastest way to get started is to download the starter project. The MEDKit starter project is a fully self-contained starter project for building and running a Twitch Extension powered by Muxy's Extension Backend Services.

- This is the same starter project Muxy uses to develop many of our client projects, now open sourced to help the community. It uses [Vue.js](https://vuejs.org) to enable quick development and provide a powerful reactive environment without too much overhead. You can modify the starter project to create basic extensions.

- If you prefer a more customized working environment, you can [install and configure MEDKit directly](docs:install-manually) with npm, node.js, and webpack. Even if you choose this approach, you might want to familiarize yourself with the structure of a MEDKit extension project by examining the starter project. 

The following are top-level files and folders you will be working with.



| Folder/File | Purpose |
| --- | --- |
| `.env` | A configurationfile containing information about your extension and testing environment. |
| `public/index.html` | The template HTML file. Your individual extension pages will use this file as a base when compiling their own pages. |
| `src/` | Source files for the extension, with subfolders for each of the individual pages that make up your project.  <br>  <br>The starter project contains two versions of a fully functioning extension.  JavaScript and TypeScript version are in the `src/js/` and src/`ts/` directories. |
| `src/{component, overlay, panel}/App.vue` | The entry point for creating an extension of the given type. |
| `src/{config, live}/App.vue` | The entry point for creating the broadcaster-only pages for an extension. |




In the starter extension, all of the files and folders are provided and built. You only need to edit the ones you actually intend to ship. For example, when building a panel extension (such as the ones in our example) you can safely ignore the `overlay/` and `component/` directories as these are used to build Overlay and Component extensions. 

> 📘 See more information about the basic types and structure of [Twitch Extensions](https://dev.twitch.tv/docs/extensions/designing/).

# Running a project

Before you can run the example project, you must have a valid Twitch Extension Client ID.  
If you don't have one, create one on [Twitch’s developer portal](https://dev.twitch.tv), choosing the Extension type. Click **Manage** to show the Client ID at top of the page. 

1. Copy the directory for the language you plan to use (`js` for JavaScript, `ts` for TypeScript) and rename it to match your extension name. This will be your _extension_root_ directory.

2. Create a file within that folder named `.env` (don't forget the beginning period on the filename), with the following content:

```text .env
VUE_APP_CLIENT_ID=<Twitch Client ID>
```

3. To compile the extension and run a local server, open a command shell, go to your _extension_root_ directory, and enter the following commands:

```shell
npm install
npm run serve
```

This makes the following component pages available. (The script prints the port number, which can differ from this example.)

- http\://localhost:4000/config.html - The broadcaster configuration
- http\://localhost:4000/live.html - The broadcaster live dashboard
- http\://localhost:4000/panel.html - The viewer panel extension
- http\://localhost:4000/component.html - The viewer component extension
- http\://localhost:4000/overlay.html - The viewer overlay extension
