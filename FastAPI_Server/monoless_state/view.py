from controller import Master_Controller as Controller
from fastapi.responses import RedirectResponse, FileResponse
from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect
import base64  # for image transfer
import uvicorn


class APP_Server:
    def __init__(self, controller:Controller):
        print("SYSTEM_CALL::APP_Server Start")
        self.app = FastAPI()
        
        self.controller = controller
        
        # middle ware accept
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # 엔드 포인트 router 실행
        self.register_routes()
        
    def register_routes(self):
        
        @self.app.get('/')
        def main():
            print("Server End point root")
            print("SYSTEM_CALL:Root System well")
            return "Server Working"
        
        @self.app.post("/login")
        def login(user_data:dict):
            self.controller.login(user_data = user_data)
        
    def run_system(self):
        uvicorn.run(app=self.app, host='127.0.0.1', port=8000)
        
        
        
        
        