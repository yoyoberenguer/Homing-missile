# encoding: utf-8
"""

                   GNU GENERAL PUBLIC LICENSE

                       Version 3, 29 June 2007


 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>

 Everyone is permitted to copy and distribute verbatim copies

 of this license document, but changing it is not allowed.
 """

import pygame
import time as time_t

if not pygame.mixer.get_init():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()


class SoundObject:

    # Sound player constructor
    def __init__(self, sound_= None, priority_= 0,
                 name_= None, channel_=None, obj_id_= None):
        """
        Define a sound player with specific attributes
        :param sound_: Sound player loaded with pygame.mixer.Sound method
        :param priority_: define a priority for the sound (low : 0. med : 1, high : 2)
        :param name_: String representing the sound name
        :param channel_: Channel number used for playing the sound
        :param obj_id_: unique sound id
        """

        self.sound = sound_                                     # pygame.mixer.Sound object (class Sound)
        self.priority = priority_ if 0 < priority_ < 2 else 0   # define the sound object priority (highest
                                                                # priority object are kept alive)
        self.time = time_t.time()                               # start time
        self.name = name_                                       # represents the sound name
        self.length = sound_.get_length()                       # Sound length in seconds
        self.active_channel = channel_                          # self.active_channel represent the numeric value
                                                                # of the channel playing the sound
        self.id = id(self)                                      # SoundObject id number
        self.obj_id = obj_id_                                   # Sound id number.


class SoundControl:
    SCREENRECT = None

    # SoundControl constructor
    def __init__(self, channel_num_=8):

        # assert isinstance(channel_num_, int), \
        #     'Expecting integer, got %s ' % type(channel_num_)

        self.channel_num = channel_num_                         # Channel number to initialized
        reserved_channel = pygame.mixer.get_num_channels()      # Reserved channels (8 unused channels)
        self.start = reserved_channel                           # First channel number
        self.end = self.channel_num + reserved_channel          # Last channel number
        pygame.mixer.set_num_channels(self.end)                 # Sets the number of available channels for the mixer.

        # The mixer can reserve any number of channels that
        # will not be automatically selected for playback by Sounds.
        # If sounds are currently playing on the reserved channels they will not be stopped.
        # This allows the application to reserve a specific number of channels for important sounds that
        # must not be dropped or have a guaranteed channel to play on.
        pygame.mixer.set_reserved(self.end)

        # Create Channels object for controlling playback
        self.channels = [pygame.mixer.Channel(j_ + self.start) for j_ in range(self.channel_num)]

        self.snd_obj = [None] * self.channel_num                # un-initialised SoundObject list
        self.channel = self.start                               # Channel index point to the origin of the stack or to
                                                                # the current channel being used
        self.all = list(range(self.start, self.end))            # Create a list of all channel number available.

    def update(self):
        """ update the SoundObject list self.snd_obj.
            iterate through all the channels to check
            if a sound is still active or not and update the SoundObject list
            accordingly. Updating the input by None for no sound being mixed.
        """
        i_ = 0
        for ch in self.channels:                 # iterate over all channels
            if ch is not None:                   # c should be a Channels object and cannot be None
                if not ch.get_busy():            # check if a sound is active
                    self.snd_obj[i_] = None
            i_ += 1

    def update_volume(self, volume_:float=1.0):
        """ Update all channels to a specific volume.
            This function does not fade the sound up or down, it
            changes the sound volume immediately.
            volume_ must be a float between 0.0 - 1.0, default is 1.0
        """
        if not(0.0 <= volume_ <= 1.0):
            volume_ = 1.0
        for ch in self.channels:          # iterate over all channels
            ch.set_volume(volume_)        # adjust volume

    def show_free_channels(self) -> list:
        """ return a list of free channels.
            Only the numeric value of the free channel
            is return.
        """
        free_channels = []
        i_ = 0
        for ch in self.channels:
            if not ch.get_busy():
                free_channels.append(i_ + self.start)
            i_ += 1
        return free_channels

    def show_sounds_playing(self):
        """
        Display all sounds objects
        """
        j_ = 0
        for object_ in self.snd_obj:
            if object_ is not None:
                print('Name :', object_.name, 'id ', object_.id, ' priority ', object_.priority,
                      ' channel ', object_.active_channel, ' length ', round(object_.length, 2),
                      ' time left : ', round(self.snd_obj[j_].length - (time_t.time() - self.snd_obj[j_].time), 2))
            j_ += 1

    def get_identical_sounds(self, sound: pygame.mixer.Sound) -> list:
        """ Return a list of channel(s) (Channel number) where identical sounds are being played.
         """
        # assert isinstance(sound, pygame.mixer.Sound), \
        #     'Expecting sound player, got %s ' % type(sound)
        list_ = []
        for obj in self.snd_obj:
            if obj is not None:
                if obj.sound == sound:
                    list_.append(obj.active_channel)
        return list_

    def get_identical_id(self, id_) -> list:
        """ Return a list containing any identical sound being mixed (using memory location).
            Provide the sound id as such id(SOUND) where sound is a pygame.mixer.Sound
            id correspond to the memory location.
         """
        # assert isinstance(sound, pygame.mixer.Sound), \
        #     'Expecting sound player, got %s ' % type(sound)
        list = []
        for obj in self.snd_obj:
            if obj is not None:
                if obj.obj_id == id_:
                    list.append(obj)
        return list

    def stop(self, list_: list=[]):
        """ stop sound(s) from a given list of channel(s).
            Only sound with priority level 0 on the given channel will be
            stopped.
         """
        for ch in list_:
                l = ch - self.start
                if self.snd_obj[l].priority == 0:
                    self.channels[l].stop()
        self.update()

    def stop_all_except(self, exception:int=None):
        """ stop all sound except sounds from a given list of id(sound)
            :exception can be a single pygame.Sound id value or a list containing
            all pygame.Sound object id numbers.
            Stop_all_except function will stop sound playing on the channel regardless
            of its priority.
        """
        if exception is None:
            return

        # create a list if exception is a single value
        exception = [exception] if isinstance(exception, int) else exception

        for ch in self.all:
            l = ch - self.start
            snd_object = self.snd_obj[l]
            if snd_object is not None:
                if snd_object.obj_id not in exception:
                    self.channels[l].stop()
        self.update()

    def stop_all(self):
        """ stop all sounds no exceptions."""
        for ch in self.all:
            l = ch - self.start
            snd_object = self.snd_obj[l]
            if snd_object is not None:
                self.channels[l].stop()
        self.update()

    def stop_name(self, name_: str=""):
        """ stop a pygame.Sound object if playing on any of the channels.
            name_ refer to the name given to the sound when instantiated (e.g 'WHOOSH' name below)
            GL.SC_spaceship.play(sound_=WHOOSH, loop_=False, priority_=0, volume_=GL.SOUND_LEVEL,
                    fade_out_ms=0, panning_=False, name_='WHOOSH', x_=0)
         """
        for sound in self.snd_obj:
            if sound is not None and sound.name == name_:
                self.channels[sound.active_channel - self.start].stop()
        self.update()

    def stop_object(self, object_id):
        """ stop a given sound using the pygame.Sound object id number. """
        for sound in self.snd_obj:
            if sound is not None and sound.obj_id == object_id:
                self.channels[sound.active_channel - self.start].stop()
        self.update()

    def show_time_left(self, object_id: int) -> float:
        """ show time left to play for a specific sound
        :param object_id: identification like e.g id(self)
        :return: a float representing the time left in seconds.
        """
        j = 0
        for obj in self.snd_obj:
            if obj is not None:
                # print(obj.name)
                # print('player_.obj_id ', obj.obj_id, ' == ', object_id)
                if obj.obj_id == object_id:
                    return round(self.snd_obj[j].length - (time_t.time() - self.snd_obj[j].time), 2)
            j += 1
        # did not found the player into the list
        # Sound probably killed, finished or wrong
        # object_id number.
        return 0.0

    def get_reserved_channels(self) -> int:
        """ return the total number of reserved channels """
        return self.channel_num

    def get_reserved_start(self) -> int:
        """ return the first reserved channel number """
        return self.start

    def get_reserved_end(self) -> int:
        """ return the last reserved channel number """
        return self.end

    def get_channels(self) -> list:
        """ return a list of all reserved pygame mixer channels.
        """
        return self.channels

    def get_sound(self, channel_: int) -> pygame.mixer.Sound:
        """ return a sound being played on a specific channel (pygame.mixer.Channel)
            channel_ is an integer representing the channel number.
        """
        # assert isinstance(channel_, int), \
        #    'Expecting integer, got %s ' % type(channel_)
        try:
            sound = self.channels[channel_]
        except IndexError:
            raise Exception('Incorrect channel number. ')
        else:
            return sound

    def get_sound_object(self, channel_: int):
        """ return a specific sound player (SoundObject) """
        # assert isinstance(channel_, int), \
        #    'Expecting integer, got %s ' % type(channel_)
        return self.snd_obj[channel_]

    def get_all_sound_object(self) -> list:
        """ return all sound objects """
        return self.snd_obj

    def play(self, sound_: pygame.mixer.Sound, loop_=False, priority_=0, volume_=1,
             fade_out_ms=0, panning_=False, name_=None,
             x_=0, object_id_=None):
        """
        :type loop_: bool
        :param sound_: pygame mixer sound player
        :param loop_:  boolean for looping sound or not (True : loop)
        :param priority_: Set the sound priority (low : 0, med : 1, high : 2)
        :param volume_:   Set the sound volume 0 to 1 (1 being full volume)
        :param fade_out_ms: Fade out sound effect in ms
        :param panning_: boolean for using panning method or not (stereo mode)
        :param name_: String representing the sound name
        :param x_:  Position for panning a sound,
        :param object_id_: unique player id
        """

        try:
            if sound_ is None:
                return
            # check if the current channel is busy.
            # if not play the given sound. <sound_>
            l = self.channel - self.start
            if self.channels[l].get_busy() == 0:

                # The fade_ms argument will make the sound start playing at 0 volume
                # and fade up to full volume over the time given. The sample may end
                # before the fade-in is complete.
                self.channels[l].play(sound_, loops=-1 if loop_ else 0, maxtime=0, fade_ms=fade_out_ms)

                self.channels[l].set_volume(volume_)
                self.snd_obj[l] = SoundObject(sound_, priority_, name_, self.channel, object_id_)

                # play a sound in stereo
                if panning_:
                    self.channels[l].set_volume(
                        self.stereo_panning(x_)[0] * volume_, self.stereo_panning(x_)[1] * volume_)

                # prepare the mixer for the next channel
                self.channel += 1
                if self.channel > self.end - 1:
                    self.channel = self.start

                # return the channel number where the sound is
                # currently playing.
                return self.channel - 1

            # All channels busy
            else:
                # print('Stopping duplicate sound on channel(s) %s %s ' % (self.get_identical_sounds(sound_), name_))
                self.stop(self.get_identical_sounds(sound_))
                # very important, go to next channel.
                self.channel += 1
                if self.channel > self.end - 1:
                    self.channel = self.start
                return None

        except IndexError as e:
            print('\n[-] SoundControl error : %s ' % e)
            print(self.channel, l)

    @staticmethod
    def stereo_panning(x_):
        # assert isinstance(x_, (float, int)), 'Expecting float got %s ' % type(x_)
        if x_ < 0:
            # do not play sound for objects outisde the screen
            return 1, 0

        elif x_ > SoundControl.SCREENRECT.w:
            return 0, 1

        else:
            right_volume = float(x_) / SoundControl.SCREENRECT.w
            left_volume = 1 - right_volume
            return left_volume, right_volume

