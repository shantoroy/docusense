import {Container, Form, InputGroup} from "react-bootstrap";

import "./ChatComponent.css";
import React from "react";
import MessageComponent from "./MessageComponent.tsx";

export interface Message {
    direction: "incoming" | "outgoing",
    message: string;
}

const ChatComponent = () => {

    const [sending, setSending] = React.useState(false);
    const [messageInput, setMessageInput] = React.useState("");
    const [messages, setMessages] = React.useState<Message[]>([]);

    const sendMessage = () => {

        setMessageInput("");

        setSending(true);

        setMessages((prev) => {
            return [...prev, {
                "direction": "outgoing",
                "message": messageInput.trim()
            },
            {
                "direction": "incoming",
                "message": messageInput.trim()
            }]
        })
    }

    return (
        <Container style={{flexDirection: "column"}} className="d-flex h-100 w-100 p-0" fluid>
            <Container style={{flexGrow: 1}} className="overflow-auto" fluid>
                {
                    messages.map((message, index) => {
                        return (
                            <MessageComponent message={message} setSending={setSending} key={index} />
                        )
                    })
                }
            </Container>
            <Container className="d-flex pb-3 message-input">
                <InputGroup>
                    <Form.Control
                        disabled={sending}
                        placeholder={"Enter your message here"}
                        className="message-input" as="textarea"
                        value={messageInput}
                        onChange={(e) => setMessageInput(e.target.value)}
                        onKeyUp={(e) => {
                            if (e.key === 'Enter')
                            {
                                // if (e.shiftKey === true)
                                if (e.shiftKey)  // thruthy
                                {
                                    // new line
                                }
                                else
                                {
                                    if(!sending && messageInput.trim().length > 0) {
                                        sendMessage();
                                    }
                                    else {
                                        setMessageInput("");
                                    }
                                }
                                return false;
                            }
                        }}
                    />
                </InputGroup>
                <Container className="d-flex align-items-center justify-content-center w-auto">
                    <button style={{border: "none", background: "transparent"}}
                            disabled={sending}
                            onClick={() => sendMessage()} >
                        <i style={{fontSize: "1.5rem",
                            color: sending || messageInput.length === 0 ? "gray" : "black", cursor: "pointer"}}
                           className="bi bi-play-circle-fill"/>
                    </button>
                </Container>

            </Container>
        </Container>
);

}

export default ChatComponent;
