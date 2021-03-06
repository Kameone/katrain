# KaTrain v1.0 (pre-release)

This repository contains a tool for analyzing and playing go with AI feedback from KataGo.

The original idea was to give immediate feedback on the many large mistakes we make in terms of inefficient moves,
but has since grown to include a wide range of features, including:

* Review your games to find the moves that were most costly in terms of points lost.
* Play against AI and get immediate feedback on mistakes with option to retry.
* Play against a wide range of weakened versions of AI with various styles.
* Play against a stronger player and use the retry option instead of handicap stones.
* Automatically generate focused SGF reviews which show your biggest mistakes.

## Screenshots

| Analyze games  | Play against an AI Teacher |
| ------------- | ------------- |
| ![screenshot](img/screenshot_analyze.png)  | ![screenshot](img/screenshot_play.png)  |

## Quickstart

* You can right-click most button or checkbox labels to get a tooltip with help.
* To analyze a game, load it using the button in the bottom right, or press `ctrl-L`
* To play against AI, pick an AI from the dropdown and either 'human' or 'teach' for yourself and start playing.
    * For different board sizes, use the button with the little goban in the bottom right for a new game.

## Installation

### Quick Installation for Windows users

See the [releases tab](https://github.com/sanderland/katrain/releases) for pre-built installers.

### Installation from source for Windows users

* Download the repository by clicking the green *Clone or download* on this page and *Download zip*. Extract the contents.
* Make sure you have a python installation, I will assume Anaconda (Python 3.7), available [here](https://www.anaconda.com/distribution/#download-section).
* Open 'Anaconda prompt' from the start menu and navigate to where you extracted the zip file using the `cd <folder>` command.
* Execute the command `pip install kivy_deps.glew kivy_deps.sdl2 kivy_deps.gstreamer kivy`
* Start the app by running `python katrain.py` in the directory where you downloaded the scripts. Note that the program can be slow to initialize the first time, due to KataGo's gpu tuning.

### Installation for Linux users

* This assumed you have a working Python 3.6/3.7 installation as a default. If your default is python 2, use pip3/python3. Kivy currently does not have a release for Python 3.8.
* Git clone or download the repository.
* Run the command `pip install kivy` in the terminal.
* A binary for KataGo is included, but if you have compiled your own, point the 'engine/katago' setting to the relevant KataGo v1.3.5-bs29+ binary.
* Start the app by running `python katrain.py`.  Note that the program can be slow to initialize the first time, due to KataGo's GPU tuning.

### Installation for MacOS users

* Download and install [Python 3.7.5](https://www.python.org/downloads/release/python-375/)
* Install [Homebrew](https://brew.sh) by running the following command in terminal
* `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
* Run the command `pip3 install kivy` in the terminal.
* Install Katago using [Homebrew](https://brew.sh/)
   * Note that the version required for Katrain is currently too new so we need to update the Homebrew script.
   * Run the command `brew edit katago` and replace lines 4-5 with
   * ```
      url "https://github.com/lightvector/KataGo/archive/v1.4.1.tar.gz"
      sha256 "b408086c7c973ddc6144e16156907556ae5f42921b9f29dc13e6909a9e9a4787"
      ```
    * You can also follow instructions [here](https://github.com/lightvector/KataGo) to compile KataGo yourself
* Now that the dependencies are installed its time to Git clone or download the katrain repository
  * Run the command `git clone https://github.com/sanderland/katrain.git` this will clone Katrain to your home folder.

* To run Katrain you need to first access the Katrain folder.
  * If you used the 'git clone' command to download the repository then its located in your home folder. You can access it by typing `cd katrain` in the terminal. If you've moved the folder to another location the easiest way to navigate to it in terminal is to type `cd` and drag the Katrain folder from the finder window into terminal. This will copy its full path to the command line.

* Now that we're in the Katrain folder run the following command. `python3 katrain.py`

The frist time you run Katrain you will see an error about initializing KataGo.

* Open the settings dialog by clicking on the gear icon at the bottom right of the window and change the path of the 'katago' setting to `/usr/local/bin/katago` (or the path where you compiled KataGo) then click 'Apply and Save'.

### Configuring the GPU KataGo uses.

  When KataGo initializes it will automatically search for OpenCL devices and select the highest scoring device. If you have multiple GPUs or want to force a specific device you will need to edit the 'analysis_config.cfg' file in the KataGo folder.

To see what devices are available and which one KataGo is using. Look for the following lines in the terminal after running `python3 katrain.py`

```
  Found 3 device(s) on platform 0 with type CPU or GPU or Accelerator
  Found OpenCL Device 0: Intel(R) Core(TM) i9-9880H CPU @ 2.30GHz (Intel) (score 102)
  Found OpenCL Device 1: Intel(R) UHD Graphics 630 (Intel Inc.) (score 6000102)
  Found OpenCL Device 2: AMD Radeon Pro 5500M Compute Engine (AMD) (score 11000102)
  Using OpenCL Device 2: AMD Radeon Pro 5500M Compute Engine (AMD) OpenCL 1.2
```

The above devices were found on a 2019 macbook pro with a discreet video card, the AMD Radeon Pro 550M. As you can see it scores about twice as high as the Intel UHD chip and KataGo has selected it as it's sole device. You can configure KataGo to use BOTH the AMD and the Intel devices to get the best performance out of the system.

* Open the 'analysis_config.cfg' file in the KataGo folder.
* Uncomment line 75 by deleting the # and setting the value to 2. The line should read `numNNServerThreadsPerModel = 2`
* Uncomment lines 117 - 118 by deleting the # and set the values to the device ID numbers identified in the terminal.

  From the example above I'v selected 1 & 2 for the Intel and AMD GPU's
```
openclDeviceToUseThread0 = 1
openclDeviceToUseThread1 = 2
```
* Run `python3 katrain.py` and confrim that KataGo is now using both devices. (Note that the first time a device is used it needs to be tuned which will take a few mintues). Below is the update output from the terminal.

```
  Found 3 device(s) on platform 0 with type CPU or GPU or Accelerator
  Found OpenCL Device 0: Intel(R) Core(TM) i9-9880H CPU @ 2.30GHz (Intel) (score 102)
  Found OpenCL Device 1: Intel(R) UHD Graphics 630 (Intel Inc.) (score 6000102)
  Found OpenCL Device 2: AMD Radeon Pro 5500M Compute Engine (AMD) (score 11000102)
  Using OpenCL Device 1: Intel(R) UHD Graphics 630 (Intel Inc.) OpenCL 1.2
  Using OpenCL Device 2: AMD Radeon Pro 5500M Compute Engine (AMD) OpenCL 1.2
```


## Manual

### Play

Under the 'play' tab you can select who is playing black and white.

* Human is simple play with potential feedback, but without auto-undo.
* Teach will give you instant feedback, and auto-undo bad moves to give you a second chance.
    * Settings for this mode can be found under 'Configure Teacher'
* AI will activate the AI in the dropdown menu next to the buttons.
    * Settings for all AIs can be found under 'Configure AIs'

If you do not want to see 'Points lost' or other feedback for your moves,
 set 'show last n dots' to 0 under 'Configure Teacher', and click on the words 'Points lost' to hide its value.

#### What are all these coloured dots?

The dots indicate how many points were lost by that move.

* The colour indicates the size of the mistake according to kata
* The size indicates if the mistake was actually punished. Going from fully punished at maximal size,
  to no actual effect on the score at minimal size.

In short, if you are a weaker player you should mostly on large dots that are red or purple,
while stronger players can pay more attention to smaller mistakes.

#### AIs

Available AIs, with strength indicating an estimate for the default settings, are:

* **[9p+]** **Default** is full KataGo, above professional level.
* **[~1k?]**  **ScoreLoss** is KataGo making moves with probability `~ e^(-strength * points lost)`, playing a varied style with small mistakes.
* **Balance** is KataGo occasionally making weaker moves, attempting to win by ~2 points.
* **Jigo** is KataGo aggressively making weaker moves, attempting to win by 0.5 points.
* **[~4d]** **Policy** uses the top move from the policy network (it's 'shape sense' without reading), should be around high dan level depending on the model used. There is a setting to increase variety in the opening, but otherwise it plays deterministically.
* **[~2k]**: **P:Weighted** picks a random move weighted by the policy, as long as it's above `lower_bound`. `weaken_fac` uses `policy^(1/weaken_fac)`, increasing the chance for weaker moves.
* **[~5k]**: **P:Pick** picks `pick_n + pick_frac *  <number of legal moves>` moves at random, and play the best move among them.
   The setting `pick_override` determines the minimum value at which this process is bypassed to play the best move instead, preventing obvious blunders.
   This, along with 'Weighted' are probably the best choice for kyu players who want a chance of winning without playing the sillier bots below. Variants of this strategy include:
    * **[~2k]**: **P:Local** will pick such moves biased towards the last move with probability related to `local_stddev`.
    * **[~10k]**: **P:Tenuki** is biased in the opposite way as P:Local, using the same setting.
    * **[~10k]**: **P:Influence** is biased towards 4th+ line moves, with every line below that dividing both the chance of considering the move and the policy value by `influence_weight`. Consider setting `pick_frac=1.0` to only affect the policy weight.
    * **[~10k]**: **P:Territory** is biased in the opposite way, towards 1-3rd line moves, using the same setting.

### Analysis

Keyboard shortcuts are shown with **[key]**.

* The checkboxes configure:
    * **[q]**: Child moves are shown. On by default, can turn it off to avoid obscuring other information or when wanting to guess the next move.
    * **[w]**: All dots: Show all evaluation dots instead of the last few.
        * You can configure how many are shown with this setting off, and whether they are shown for AIs under 'Play/Configure Teacher'.
    * **[e]**: Top moves: Show the next moves KataGo considered, colored by their expected point loss. Small dots indicate high uncertainty. Hover over any of them to see the principal variation.
    * **[r]**: Show owner: Show expected ownership of each intersection.
    * **[t]**: NN Policy: Show KataGo's policy network evaluation, i.e. where it thinks the best next move is purely from the position, and in the absence of any 'reading'.

* The analysis buttons are used for:
    * **[a]**: Extra: Re-evaluate the position using more visits, usually resulting in a more accurate evaluation.
    * **[s]**: Equalize: Re-evaluate all currently shown next moves with the same visits as the current top move. Useful to increase confidence in the suggestions with high uncertainty.
    * **[d]**: Sweep: Evaluate all possible next moves. This can take a bit of time even though 'fast_visits' is used, but the result is nothing if not colourful.

## Keyboard and mouse shortcuts

In addition to shortcuts mentioned above, there are:

* **[Tab]**: to switch between analysis and play modes. (NB. keyboard shortcuts function regardless)
* **[~]** or **[`]** or **[p]**: Hide side panel UI and only show the board.
* **[enter]**: AI Move
* **[arrow up]** or **[z]**: Undo move. Hold shift for 10 moves at a time, or ctrl to skip to the start.
* **[arrow down]** or **[x]**: Redo move. Hold shift for 10 moves at a time, or ctrl to skip to the start.
* **[scroll up]**: Undo move. Only works when hovering the cursor over the board.
* **[scroll down]**: Redo move. Only works when hovering the cursor over the board.
* **[click on a move]**: See detailed statistics for a previous move.
* **[double-click on a move]**: Navigate directly to that point in the game.
* **[Ctrl-v]**: Load SGF from clipboard and do a 'fast' analysis of the game (with a high priority normal analysis for the last move).
* **[Ctrl-c]**: Save SGF to clipboard.
* **[Ctrl-l]**: Load SGF from file and do a normal analysis.
* **[Ctrl-s]**: Save SGF with automated review to file.
* **[Ctrl-n]**: Load SGF from clipboard
* **[space]**: Pass

## Configuration

Configuration is stored in `config.json`. Most settings are now available to edit in the program, but some advanced options are not.
You can use `python katrain.py your_config_file.json` to use another config file instead.

If you ever need to reset to the original settings, simply re-download the `config.json` file in this repository.

### Settings Panel

* engine settings
    * These settings can be updated anytime:
        * max_visits: The number of visits used in analyses and AI moves, higher is more accurate but slower.
        * max_time: Maximal time in seconds for analyses, even when the target number of visits has not been reached.    
        * fast_visits: The number of visits used for certain operations with fewer visits.
        * wide_root_noise: Consider a wider variety of moves, using KataGo's `analysisWideRootNoise` option. Will affect both analysis and AIs such as ScoreLoss. (KataGo 1.4+ only, keep at 0.0 otherwise)
    * These settings cause the engine to be restarted:
        * katago: Path to your KataGo executable.
        * model: Path to your KataGo model file. Note that the default model file included is an older 15 block one for high speed and low memory requirements. Replace it with a new model from [here](https://github.com/lightvector/KataGo/releases) for maximal strength.
        * config: Path to your KataGo config file.    
        * threads: Number of threads to use in the KataGo analysis engine.
* game settings
    * init_size: the initial size of the board, on start-up.
    * init_komi: likewise, for komi.
* sgf settings
    * sgf_load: default path where the load SGF dialog opens.
    * sgf_save: path where SGF files are saved.    
* board_ui settings
    * eval_dot_max_size: size of coloured dots when point size is maximal, relative to stone size.
    * eval_dot_min_size: size of coloured dots when point size is minimal
    * ... various other minor cosmetic options.
* debug settings
    * level: determines the level of output in the console, where 0 shows no debug output, 1 shows some and 2 shows a lot. This is mainly used for reporting bugs.

## FAQ

* Why is the program is slow to start.
  * The first startup of KataGo can be slow due to GPU tuning, after that it should be much faster.
* The program is running too slowly. How can I speed it up?
  *  Adjust the number of visits or maximum time allowed in the settings.
* KataGo crashes with out of memory errors, how can I prevent this?
  *  Try using a lower number for `nnMaxBatchSize` in `KataGo/analysis_config.cfg`, and avoid using versions compiled with large board sizes.

## Contributing

* Feedback and pull requests are both very welcome. I would also be happy to host translations of this manual into languages where English fluency is typically lower.
* For suggestions and planned improvements, see the 'issues' tab on github.
* You can also contact me on discord (Sander#3278), [KakaoTalk](https://open.kakao.com/o/gTsMJCac) or [Reddit](http://reddit.com/u/sanderbaduk) to give feedback, or simply show your appreciation.
* Some people have also asked me how to donate. Something go-related such as a book or teaching time is highly appreciated.
