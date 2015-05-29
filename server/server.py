import pushbullet
import transmissionrpc
import sys


#################################
DEVICE_NAME='Pushtorrent Server'
TRANSMISSION_IP='127.0.0.1'
TRANSMISSION_PORT=9091
TRANSMISSION_USER=''
TRANSMISSION_PASSWORD=''
API_KEY=''
#################################

#TODO: Read settings from external file

class PushtorrentServer:

    def __init__(self):
        print('Starting pushtorrent server.')
        print('Connecting to pushbullet...')
        self.pb=pushbullet.Pushbullet(API_KEY)
        print('Connecting to torrent client...')
        self.torclient=transmissionrpc.Client(address=TRANSMISSION_IP,port=TRANSMISSION_PORT,user=TRANSMISSION_USER,password=TRANSMISSION_PASSWORD)
        print('Creating device...')
        self.pb.new_device(DEVICE_NAME) #TODO: Check if device already exists before creating
        print('Finishing setup...')
        self.listener=pushbullet.Listener(self.pb,on_push=self.onListener)   
        self.listener.run_forever()

    def onListener(self,notification):
        if notification.get(u'type') == u'tickle':
            notification=self.pb.get_pushes()[1][0]
        if u'title' in notification.keys() and notification.get(u'title').upper()==u'ADD TORRENT' and not notification.get(u'dismissed'):
            if notification.get(u'type')==u'link' or notification.get(u'type')==u'file':
                torrentfile=str(notification.get(u'url'))
                print('Adding file {0}'.format(torrentfile))
                self.torclient.add_torrent(torrentfile)

if __name__=='__main__':
    PushtorrentServer()

        

