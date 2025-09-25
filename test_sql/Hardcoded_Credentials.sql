DECLARE @db_user NVARCHAR(50) = 'app_user';
DECLARE @db_pass NVARCHAR(50) = 'SuperSecret123';   -- ❌ Exposed credential

-- Attempting connection
EXEC sp_addlinkedserver 
   @server = 'RemoteDB',
   @provider = 'SQLNCLI',
   @datasrc = '192.168.1.100';

EXEC sp_addlinkedsrvlogin 
   @rmtsrvname = 'RemoteDB',
   @useself = 'false',
   @locallogin = NULL,
   @rmtuser = @db_user,
   @rmtpassword = @db_pass;
