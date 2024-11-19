import {Container} from "react-bootstrap";
import LLMResponse from "../LLMResponseComponent/LLMResponse.tsx";
import {Message} from "./ChatComponent.tsx";
import React from "react";

interface MessageComponentProps {
    message: Message,
    setSending: React.Dispatch<boolean>
}

const MessageComponent =
    ( {message, setSending}: MessageComponentProps ) => {
    return (
        <Container className="d-flex flex-row">
            <Container style={{width: "fit-content"}}>
                {message.direction === "outgoing" && <i style={{fontSize: "2rem"}} className="bi bi-person-fill"/>}
                {message.direction === "incoming" && <i style={{fontSize: "2rem"}} className="bi bi-robot"/>}
            </Container>
            <Container className="d-flex flex-column p-2">
                <strong><p>{message.direction === "outgoing" ? "You" : "Model"}</p></strong>
                {message.direction === "incoming" &&
                    <LLMResponse chat_message={message.message} chat_name="test" set_sending={setSending} />}
                {message.direction === "outgoing" && <p>{message.message}</p>}
            </Container>
        </Container>
    );
}

export default MessageComponent;
