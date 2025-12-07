import { WebSocketServer } from 'ws';

export function setupTranscriptSocket(server: any) {
  const wss = new WebSocketServer({ server, path: '/ws/transcript' });
  wss.on('connection', (socket) => {
    socket.on('message', (data) => {
      wss.clients.forEach((client) => {
        if (client.readyState === 1) {
          client.send(data.toString());
        }
      });
    });
  });
  return wss;
}
