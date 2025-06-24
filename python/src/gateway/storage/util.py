import pika, json

def upload(file, fs, channel, access):
    # I) upload a file to the mongoDB using gridFS(fs)
    try:
        fid = fs.put(file)
    except Exception as err:
        print(err)
        return f"internal server error {err}", 500

    # II) once the file has been uploaded - put a message into a RabbitMQ queue
    message = {
        "video_fid": str(fid), #used for upload
        "mp3_fid": None, #used for download
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange = "",
            routing_key="video",
            body=json.dumps(message), # serialize a python object to json string
            properties=pika.BasicProperties(
                # queue and messages in it are durable
                #  if pod crashes or restart, messages will be persistet
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE 
            ),
        )
    except Exception as err:  
        print(err)
        fs.delete(fid)
        return f"internal server error: {err}", 500