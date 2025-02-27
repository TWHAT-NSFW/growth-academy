
## Music Room ##################################################################
##
## This controls the music room player positions, sizes and more.

## The positions and sizes of the music viewport list
define gui.music_room_viewport_xsize = int(250 * ost.scale)
define gui.music_room_viewport_pos = int(20 * ost.scale)
define gui.music_room_spacing = int(20 * ost.scale)
define gui.music_room_viewport_ysize = 0.93

## The positions and sizes of the music information text
define gui.music_room_information_xpos = int(700 * ost.scale)
define gui.music_room_information_ypos = int(220 * ost.scale)
define gui.music_room_information_xsize = int(580 * ost.scale)

## The positions and sizes of the music controls
define gui.music_room_options_xpos = int(715 * ost.scale)
define gui.music_room_options_ypos = int(410 * ost.scale)
define gui.music_room_options_spacing = int(20 * ost.scale)
define gui.music_room_options_button_size = int(36 * ost.scale)

## The positions of the music settings controls
define gui.music_room_settings_ypos = int(450 * ost.scale)

## The positions and sizes of the music progress bar
define gui.music_room_progress_xsize = int(710 * ost.scale)
define gui.music_room_progress_xpos = int(330 * ost.scale)
define gui.music_room_progress_ypos = int(520 * ost.scale)

## The positions and sizes of the music volume bar
define gui.music_room_volume_xsize = int(120 * ost.scale)
define gui.music_room_volume_xpos = int(1130 * ost.scale)
define gui.music_room_volume_options_xpos = int(1090 * ost.scale)
define gui.music_room_volume_options_ypos = int(509 * ost.scale)

## The positions for the music progress/duration time text
define gui.music_room_progress_text_xpos = int(330 * ost.scale)
define gui.music_room_text_size = gui.interface_text_size
define gui.music_room_duration_text_xpos = int(975 * ost.scale)
define gui.music_room_progress_text_ypos = int(550 * ost.scale)

## The positions for the cover art and it's transform properties
define gui.music_room_cover_art_xpos = int(500 * ost.scale)
define gui.music_room_cover_art_ypos = int(300 * ost.scale)
define gui.music_room_cover_art_size = int(350 * ost.scale)

init python:

    if renpy.variant('small'):
        gui.music_room_text_size = int(24 * ost.scale)
        gui.music_room_progress_text_ypos = int(560 * ost.scale)
        gui.music_room_volume_options_xpos = int(1080 * ost.scale)
        gui.music_room_volume_options_ypos = int(514 * ost.scale)
        gui.music_room_options_button_size = int(40 * ost.scale)

image readablePos = DynamicDisplayable(renpy.curry(ost.music_pos)("music_room_progress_text"))
image readableDur = DynamicDisplayable(renpy.curry(ost.music_dur)("music_room_duration_text"))
image titleName = DynamicDisplayable(renpy.curry(ost.dynamic_title_text)("music_room_information_text"))
image authorName = DynamicDisplayable(renpy.curry(ost.dynamic_author_text)("music_room_information_text"))
image coverArt = DynamicDisplayable(ost.refresh_cover_data)
image songDescription = DynamicDisplayable(renpy.curry(ost.dynamic_description_text)("music_room_information_text"))
image rpa_map_warning = DynamicDisplayable(renpy.curry(ost.rpa_mapping_detection)("music_room_information_text"))
image playPauseButton = DynamicDisplayable(ost.auto_play_pause_button)

screen music_room():

    tag menu
    add "Graphics/ui/bg/archiveBG/music_eve.png"

    default bar_val = ost.AdjustableAudioPositionValue()

    style_prefix "music_room"

    add gui.main_menu_background
    on "replaced" action Play("music", "Audio/BGM/hallowedhalls.ogg")

    frame:
        style "music_room_frame"

    side "c l":

        viewport id "vpo":

            style "music_room_viewport"

            mousewheel True
            has vbox

            spacing gui.navigation_spacing

            for st in ost.soundtracks:
                textbutton "[st.name]":
                    text_style "music_room_button"
                    if ost.game_soundtrack:
                        action [SensitiveIf(ost.game_soundtrack.name != st.name or ost.game_soundtrack.author != st.author or ost.game_soundtrack.description != st.description), SetVariable("ost.game_soundtrack", st), Play("music_room", st.path, loop=ost.loopSong, fadein=2.0)]
                    else:
                        action [SetVariable("ost.game_soundtrack", st), Play("music_room", st.path, loop=ost.loopSong, fadein=2.0)]

        vbar value YScrollValue("vpo") xpos 1.0 ypos 20

    if ost.game_soundtrack:

        if ost.game_soundtrack.cover_art:

            add "coverArt" at cover_art_fade

        if ost.game_soundtrack.author:

            vbox:

                hbox:
                    vbox:
                        add "titleName"

                hbox:
                    vbox:
                        add "authorName"

                if ost.game_soundtrack.description:
                    hbox:
                        vbox:
                            add "songDescription"

        hbox:
            style "music_room_control_options"

            imagebutton:
                idle At("Graphics/ui/icons/backward.png", imagebutton_scale)
                action [SensitiveIf(renpy.music.is_playing(channel='music_room')), Function(ost.current_music_backward)]

            add "playPauseButton" at imagebutton_scale

            imagebutton:
                idle At("Graphics/ui/icons/forward.png", imagebutton_scale)
                action [SensitiveIf(renpy.music.is_playing(channel='music_room')), Function(ost.current_music_forward)]

        hbox:

            style "music_room_setting_options"

            imagebutton:
                idle At(ConditionSwitch("ost.organizeAZ", "Graphics/ui/icons/A-ZOn.png", "True", "Graphics/ui/icons/A-Z.png"), imagebutton_scale)
                action [ToggleVariable("ost.organizeAZ", False, True), Function(ost.resort)]

            imagebutton:
                idle At(ConditionSwitch("ost.organizePriority", "Graphics/ui/icons/priorityOn.png", "True", "Graphics/ui/icons/priority.png"), imagebutton_scale)
                action [ToggleVariable("ost.organizePriority", False, True), Function(ost.resort)]

            imagebutton:
                idle At(ConditionSwitch("ost.loopSong", "Graphics/ui/icons/replayOn.png", "True", "Graphics/ui/icons/replay.png"), imagebutton_scale)
                action [ToggleVariable("ost.loopSong", False, True)]

            imagebutton:
                idle At(ConditionSwitch("ost.randomSong", "Graphics/ui/icons/shuffleOn.png", "True", "Graphics/ui/icons/shuffle.png"), imagebutton_scale)
                action [ToggleVariable("ost.randomSong", False, True)]

            imagebutton:
                idle At("Graphics/ui/icons/refreshList.png", imagebutton_scale)
                action [Function(ost.refresh_list)]

        bar:
            style "music_room_progress_bar"
            value bar_val
            hovered bar_val.hovered
            unhovered bar_val.unhovered

        bar value Preference ("music_room_mixer volume") style "music_room_volume_bar"

        imagebutton:
            style "music_room_volume_options"
            idle At(ConditionSwitch("preferences.get_volume(\"music_room_mixer\") == 0.0", "Graphics/ui/icons/volume.png", "True", "Graphics/ui/icons/volumeOn.png"), imagebutton_scale)
            action [Function(ost.mute_player)]

        add "readablePos"
        add "readableDur"

    text "Ren'Py Universal Player v[ost.version]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        size gui.notify_text_size

    if not config.developer:
        add "rpa_map_warning" xpos 0.23 ypos 0.85 xsize 950

    textbutton _("Return"):
        style "return_button"

        action [ShowMenu("extras"), If(renpy.music.is_playing(channel='music_room'), true=Function(ost.current_music_pause), false=None), If(ost.prevTrack == False, true=None, false=Play('music', ost.prevTrack, fadein=2.0))]

style music_room_frame is empty
style music_room_viewport is gui_viewport
style music_room_progress_bar is gui_slider
style music_room_volume_bar is gui_slider
style music_room_volume_options is gui_button
style music_room_button is gui_button
style music_room_control_options is gui_button
style music_room_setting_options is gui_button
style music_room_information_text is gui_text
style music_room_progress_text is gui_text
style music_room_duration_text is gui_text

style music_room_frame:
    yfill True

    background "Graphics/ui/bg/archiveBG/music_eve.png"
    foreground "gui/overlay/game_menu.png"

style music_room_button is default:
    font gui.text_font
    size gui.interface_text_size
    hover_color gui.hover_color
    selected_color gui.selected_color
    insensitive_color gui.insensitive_color
    line_spacing 5

style music_room_viewport:
    xpos gui.music_room_viewport_pos
    ypos gui.music_room_viewport_pos
    xsize gui.music_room_viewport_xsize
    ysize gui.music_room_viewport_ysize

style music_room_information_text:
    font gui.interface_text_font
    xpos gui.music_room_information_xpos
    ypos gui.music_room_information_ypos
    xsize gui.music_room_information_xsize
    xfill True

style music_room_control_options:
    xpos gui.music_room_options_xpos
    ypos gui.music_room_options_ypos
    spacing gui.music_room_spacing

style music_room_setting_options is music_room_control_options:
    ypos gui.music_room_settings_ypos

style music_room_progress_bar:
    xsize gui.music_room_progress_xsize
    xpos gui.music_room_progress_xpos
    ypos gui.music_room_progress_ypos

style music_room_volume_bar:
    xsize gui.music_room_volume_xsize
    xpos gui.music_room_volume_xpos
    ypos gui.music_room_progress_ypos

style music_room_volume_options:
    xpos gui.music_room_volume_options_xpos
    ypos gui.music_room_volume_options_ypos

style music_room_progress_text:
    font gui.interface_text_font
    xpos gui.music_room_progress_text_xpos
    ypos gui.music_room_progress_text_ypos
    size gui.music_room_text_size

style music_room_duration_text is music_room_progress_text:
    xpos gui.music_room_duration_text_xpos

transform cover_art_fade:
    anchor (0.5, 0.5)
    xpos gui.music_room_cover_art_xpos
    ypos gui.music_room_cover_art_ypos
    size (gui.music_room_cover_art_size, gui.music_room_cover_art_size)
    alpha 0
    linear 0.2 alpha 1

transform imagebutton_scale:
    size(gui.music_room_options_button_size, gui.music_room_options_button_size)
