import processamento_de_imagem

videoPath = "./videos/noite.mp4"

lane_assist = processamento_de_imagem.LaneAssist(videoPath)
lane_assist.sentinel_mode()
