import { notification } from "antd";
import React, { createContext, useContext } from "react";
import { useDispatch } from "react-redux";
import { rootActions } from "../../../Redux/Root/rootActions";

const NotificationContext = createContext(null);

export const useNotification = () => useContext(NotificationContext);

export const Notification = ({ children }) => {
  const [api, contextHolder] = notification.useNotification();
  const dispatch = useDispatch();
  const openNotification = (message, description, type) => {
    api[type]({
      message,
      description,
      onClose: handleNotificationClose,
      placement: "top",
    });
  };
  const handleNotificationClose = () => {
    dispatch(rootActions.excelActions.storeError(null));
  };
  const value = { openNotification };

  return (
    <NotificationContext.Provider value={value}>
      {contextHolder}
      {children}
    </NotificationContext.Provider>
  );
};
